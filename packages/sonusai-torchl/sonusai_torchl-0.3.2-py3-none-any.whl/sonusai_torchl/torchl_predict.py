"""sonusai torchl_predict

usage: torchl_predict [-hvrw] [-i MIXID] [-a ACCEL] [-p PREC] [-d DLCPU] [-m MODEL]
                      (-k CKPT) [-b BATCH] [-t TSTEPS] DATA ...

options:
    -h, --help
    -v, --verbose                   Be verbose.
    -i MIXID, --mixid MIXID         Mixture ID(s) to use if input is a mixture database. [default: *].
    -a ACCEL, --accelerator ACCEL   Accelerator to use in PL trainer in non-reset mode [default: auto]
    -p PREC, --precision PREC       Precision to use in PL trainer in non-reset mode. [default: 32]
    -d DLCPU, --dataloader-cpus     Number of workers/cpus for dataloader. [default: 0]
    -m MODEL, --model MODEL         PL model .py file path.
    -k CKPT, --checkpoint CKPT      PL checkpoint file with weights.
    -b BATCH, --batch BATCH         Batch size (deprecated and forced to 1). [default: 1]
    -t TSTEPS, --tsteps TSTEPS      Timesteps. If 0, dim is not included/expected in model. [default: 0]
    -r, --reset                     Reset model between each file.
    -w, --wavdbg                    Write debug .wav files of feature input, truth, and predict. [default: False]

Run PL (Pytorch Lightning) prediction with model and checkpoint input using input data from a
SonusAI mixture database.
The PL model is imported from MODEL .py file and weights loaded from checkpoint file CKPT.

Inputs:
    ACCEL       Accelerator used for PL prediction. As of PL v2.0.8:  auto, cpu, cuda, hpu, ipu, mps, tpu
    PREC        Precision used in PL prediction. PL trainer will convert model+weights to specified prec.
                As of PL v2.0.8:
                ('16-mixed', 'bf16-mixed', '32-true', '64-true', 64, 32, 16, '64', '32', '16', 'bf16')
    MODEL       Path to a .py with MyHyperModel PL model class definition
    CKPT        A PL checkpoint file with weights.
    DATA       The input data must be one of the following:
                * directory
                  Use SonusAI mixture database directory, generate feature and truth data if not found.
                  Run prediction on the feature. The MIXID is required (or default which is *)

                * Single WAV file or glob of WAV files
                  Using the given model, generate feature data and run prediction. A model file must be
                  provided. The MIXID is ignored.

Outputs the following to tpredict-<TIMESTAMP> directory:
    <id>.h5
        dataset:    predict
    torch_predict.log

"""
import signal
import sys
from os import makedirs
from os.path import abspath
from os.path import basename
from os.path import isdir
from os.path import join
from os.path import normpath
from os.path import realpath
from os.path import splitext
from typing import Any

import h5py
import torch
from docopt import docopt
from lightning.pytorch import Trainer
from lightning.pytorch.callbacks import BasePredictionWriter
from pyaaware import FeatureGenerator
from pyaaware import TorchInverseTransform
from sonusai import create_file_handler
from sonusai import initial_log_messages
from sonusai import logger
from sonusai import update_console_handler
from sonusai.mixture import Feature
from sonusai.mixture import MixtureDatabase
from sonusai.mixture import get_audio_from_feature
from sonusai.mixture import get_feature_from_audio
from sonusai.mixture import read_audio
from sonusai.utils import PathInfo
from sonusai.utils import braced_iglob
from sonusai.utils import create_ts_name
from sonusai.utils import trim_docstring
from sonusai.utils import write_wav
from torchinfo import summary

import sonusai_torchl
from sonusai_torchl.data_generator import TorchFromMixtureDatabase
from sonusai_torchl.utils.torchl_utils import torchl_build_model
from sonusai_torchl.utils.torchl_utils import torchl_hparam_override
from sonusai_torchl.utils.torchl_utils import torchl_load_ckpt
from sonusai_torchl.utils.torchl_utils import torchl_load_litmodel


def signal_handler(_sig, _frame):
    logger.info('Canceled due to keyboard interrupt')
    sys.exit(1)


signal.signal(signal.SIGINT, signal_handler)


class CustomWriter(BasePredictionWriter):
    def __init__(self, output_dir, write_interval):
        super().__init__(write_interval)
        self.output_dir = output_dir

    def write_on_epoch_end(self, trainer, pl_module, predictions, batch_indices):

        # this will create N (num processes) files in `output_dir` each containing
        # the predictions of its respective rank
        # torch.save(predictions, os.path.join(self.output_dir, f"predictions_{trainer.global_rank}.pt"))

        # optionally, you can also save `batch_indices` to get the information about the data index
        # from your prediction data
        num_dev = len(batch_indices)
        logger.debug(f'Num dev: {num_dev}, prediction writer global rank: {trainer.global_rank}')
        len_pred = len(predictions)  # for debug, should be num_dev
        logger.debug(f'len predictions: {len_pred}, len batch_indices0 {len(batch_indices[0])}')
        logger.debug(f'Prediction writer batch indices: {batch_indices}')

        logger.info(f'Predictions returned: {len(predictions)}, writing to .h5 files ...')
        for ndi in range(num_dev):  # iterate over list devices (num of batch groups)
            num_batches = len(batch_indices[ndi])  # num batches in dev
            for bi in range(num_batches):  # iterate over list of batches per dev
                bsz = len(batch_indices[ndi][bi])  # batch size
                for di in range(bsz):
                    gid = batch_indices[0][bi][di]
                    # gid = (bgi+1)*bi + bi
                    # gid = bgi + bi
                    logger.debug(f'{ndi}, {bi}, {di}: global id: {gid}')
                    output_name = join(self.output_dir, trainer.predict_dataloaders.dataset.mixdb.mixtures[gid].name)
                    # output_name = join(output_dir, mixdb.mixtures[i].name)
                    pdat = predictions[bi][di, None].cpu().numpy()
                    logger.debug(f'Writing predict shape {pdat.shape} to {output_name}')
                    with h5py.File(output_name, 'a') as f:
                        if 'predict' in f:
                            del f['predict']
                        f.create_dataset('predict', data=pdat)

        # output_name = join(self.output_dir,trainer.predict_dataloaders.dataset.mixdb.mixtures[0].name)
        # logger.debug(f'Writing predict shape {pdat.shape} to {output_name}')
        # torch.save(batch_indices, os.path.join(self.output_dir, f"batch_indices_{trainer.global_rank}.pt"))


def power_compress(x):
    real = x[..., 0]
    imag = x[..., 1]
    spec = torch.complex(real, imag)
    mag = torch.abs(spec)
    phase = torch.angle(spec)
    mag = mag ** 0.3
    real_compress = mag * torch.cos(phase)
    imag_compress = mag * torch.sin(phase)
    return torch.stack([real_compress, imag_compress], 1)


def power_uncompress(real, imag):
    spec = torch.complex(real, imag)
    mag = torch.abs(spec)
    phase = torch.angle(spec)
    mag = mag ** (1. / 0.3)
    real_compress = mag * torch.cos(phase)
    imag_compress = mag * torch.sin(phase)
    return torch.stack([real_compress, imag_compress], -1)


def main() -> None:
    args = docopt(trim_docstring(__doc__), version=sonusai_torchl.__version__, options_first=True)

    verbose = args['--verbose']
    mixids = args['--mixid']
    accel = args['--accelerator']
    prec = args['--precision']
    dlcpu = int(args['--dataloader-cpus'])
    model_path = args['--model']
    ckpt_path = args['--checkpoint']
    batch_size = args['--batch']
    timesteps = args['--tsteps']
    reset = args['--reset']
    wavdbg = args['--wavdbg']  # write .wav if true
    datapaths = args['DATA']

    if batch_size is not None:
        batch_size = int(batch_size)
    if batch_size != 1:
        batch_size = 1
        logger.info(f'For now prediction only supports batch_size = 1, forcing it to 1 now')

    if timesteps is not None:
        timesteps = int(timesteps)

    # Import checkpoint file first to check
    ckpt, hparams, ckpt_base, ckpt_root = torchl_load_ckpt(ckpt_path)
    # Import model file, expects Sonusai convention of a PL class named MyHyperModel
    litmodel, model_base, model_root = torchl_load_litmodel(model_path)

    mixdb_path = None
    entries = None
    if len(datapaths) == 1 and isdir(datapaths[0]):  # Assume it's a single path to sonusai mixdb subdir
        in_basename = basename(normpath(datapaths[0]))
        mixdb_path = datapaths[0]
        logger.debug(f'Attempting to load mixture database from {mixdb_path}')
        mixdb = MixtureDatabase(mixdb_path)
        logger.debug(
            f'Sonusai mixture db load success: found {mixdb.num_mixtures} mixtures with {mixdb.num_classes} classes')
        p_mixids = mixdb.mixids_to_list(mixids)
        if len(p_mixids) != mixdb.num_mixtures:
            logger.info(f'Processing a subset of {p_mixids} from available mixtures.')
    else:  # search all datapaths for .wav, .flac (or whatever is specified in include)
        in_basename = ''
        entries: list[PathInfo] = []
        for p in datapaths:
            location = join(realpath(abspath(p)), '**', include)
            logger.debug(f'Processing {location}')
            for file in braced_iglob(pathname=location, recursive=True):
                name = file
                entries.append(PathInfo(abs_path=file, audio_filepath=name))

    output_dir = create_ts_name('tpredict-' + in_basename)
    makedirs(output_dir, exist_ok=True)

    # Setup logging file
    logger.info(f'Created output subdirectory {output_dir}')
    create_file_handler(join(output_dir, 'torchl_predict.log'))
    update_console_handler(verbose)
    initial_log_messages('torchl_predict', subprocess=sonusai_torchl.__version__)
    logger.info(f'torch    {torch.__version__}')
    logger.info(f'Imported model from {model_base}')
    logger.info(f'Loaded checkpoint from {ckpt_base}')
    # Override hyper-parameters, especially batch_size and timesteps, return timesteps which returns model status
    hparams, timesteps = torchl_hparam_override(hparams, batch_size, timesteps)
    # Build model, updates hparams for missing SonusAI params (need for model prediction feature gen compatibility)
    model, hparams = torchl_build_model(litmodel, hparams, training=False, ckpt=ckpt)

    logger.info('')
    logger.info(summary(model))
    logger.info('')
    logger.info(f'feature       {model.hparams.feature}')
    logger.info(f'num_classes   {model.num_classes}')
    logger.info(f'batch_size    {model.hparams.batch_size}')
    logger.info(f'timesteps     {model.hparams.timesteps}')
    logger.info(f'flatten       {model.flatten}')
    logger.info(f'add1ch        {model.add1ch}')
    logger.info(f'truth_mutex   {model.truth_mutex}')
    logger.info(f'input_shape   {model.input_shape}')
    logger.info('')
    model.eval()

    logger.info('')
    if mixdb_path is not None:  # mixdb input, already loaded
        if hparams["feature"] != mixdb.feature:  # Check mixdb feature, etc. is what model expects
            logger.warning(f'Mixture feature does not match model feature, this inference run may fail.')
        feature_mode = mixdb.feature  # no choice, can't use hparams["feature"] since it's different than the mixdb
        p_mixids = mixdb.mixids_to_list(mixids)
        sampler = None
        p_datagen = TorchFromMixtureDatabase(mixdb=mixdb,
                                             mixids=p_mixids,
                                             batch_size=model.hparams.batch_size,
                                             cut_len=0,
                                             flatten=model.flatten,
                                             add1ch=model.add1ch,
                                             random_cut=False,
                                             sampler=sampler,
                                             drop_last=False,
                                             num_workers=dlcpu)

        # Info needed to set up inverse transform
        half = model.num_classes // 2
        fg = FeatureGenerator(feature_mode=model.hparams.feature,
                              num_classes=model.num_classes,
                              truth_mutex=model.truth_mutex)
        itf = TorchInverseTransform(N=fg.itransform_N,
                                    R=fg.itransform_R,
                                    bin_start=fg.bin_start,
                                    bin_end=fg.bin_end,
                                    ttype=fg.itransform_ttype)

        enable_truth_wav = False
        enable_mix_wav = False
        if wavdbg:
            if mixdb.target_files[0].truth_settings[0].function == 'target_mixture_f':
                enable_mix_wav = True
                enable_truth_wav = True
            elif mixdb.target_files[0].truth_settings[0].function == 'target_f':
                enable_truth_wav = True

        if reset:
            logger.info(f'Running {mixdb.num_mixtures} mixtures individually with model reset ...')
            for idx, val in enumerate(p_datagen):
                # truth = val[1]
                feature = val[0]
                with torch.no_grad():
                    ypred = model(feature)
                output_name = join(output_dir, mixdb.mixtures[idx].name)
                pdat = ypred.detach().numpy()
                if timesteps > 0:
                    logger.debug(f'In and out tsteps: {feature.shape[1]},{pdat.shape[1]}')
                logger.debug(f'Writing predict shape {pdat.shape} to {output_name}')
                with h5py.File(output_name, 'a') as f:
                    if 'predict' in f:
                        del f['predict']
                    f.create_dataset('predict', data=pdat)

                if wavdbg:
                    owav_base = splitext(output_name)[0]
                    tmp = torch.complex(ypred[..., :half], ypred[..., half:]).permute(2, 0, 1).detach()
                    itf.reset()
                    predwav, _ = itf.execute_all(tmp)
                    # predwav, _ = calculate_audio_from_transform(tmp.numpy(), itf, trim=True)
                    write_wav(owav_base + '.wav', predwav.permute([1, 0]).numpy(), 16000)
                    if enable_truth_wav:
                        # Note this support truth type target_f and target_mixture_f
                        tmp = torch.complex(val[0][..., :half], val[0][..., half:2 * half]).permute(2, 0, 1).detach()
                        itf.reset()
                        truthwav, _ = itf.execute_all(tmp)
                        write_wav(owav_base + '_truth.wav', truthwav.permute([1, 0]).numpy(), 16000)

                    if enable_mix_wav:
                        tmp = torch.complex(val[0][..., 2 * half:3 * half], val[0][..., 3 * half:]).permute(2, 0, 1)
                        itf.reset()
                        mixwav, _ = itf.execute_all(tmp.detach())
                        write_wav(owav_base + '_mix.wav', mixwav.permute([1, 0]).numpy(), 16000)

        else:
            # Preferred method, use builtin lightning prediction loop, returns a list to write_on_epoch in pred_writer
            logger.info(f'Running {mixdb.num_mixtures} mixtures with model builtin prediction loop ...')
            pred_writer = CustomWriter(output_dir=output_dir, write_interval="epoch")
            trainer = Trainer(default_root_dir=output_dir,
                              callbacks=[pred_writer],
                              precision=prec,
                              devices='auto',
                              accelerator=accel)  # prints avail GPU, TPU, IPU, HPU and selected device
            # logger.info(f'Strategy: {trainer.strategy.strategy_name}')  # doesn't work for ddp strategy
            logger.info(f'Accelerator stats: {trainer.accelerator.get_device_stats(device=None)}')
            logger.info(f'World size: {trainer.world_size}')
            logger.info(f'Nodes: {trainer.num_nodes}')
            logger.info(f'Devices: {trainer.accelerator.auto_device_count()}')

            # Use builtin lightning prediction loop, returns a list
            # predictions = trainer.predict(model, p_datagen)  # standard method, but no support distributed
            with torch.no_grad():
                trainer.predict(model, p_datagen)
            # predictions = model.predict_outputs
            # pred_batch_idx = model.predict_batch_idx
            # if trainer.world_size > 1:
            #     ddp_max_mem = torch.cuda.max_memory_allocated(trainer.local_rank) / 1000
            #     logger.info(f"GPU {trainer.local_rank} max memory using DDP: {ddp_max_mem:.2f} MB")
            # if not trainer.is_global_zero:
            #     return
            # logger.debug(f'type predictions: {type(predictions)}, type batch_idx: {type(pred_batch_idx)}')
            # logger.debug(f'# predictions: {len(predictions)}, # batch_idx: {len(pred_batch_idx)}')
            # logger.debug(f'{pred_batch_idx}')
            # # # all_predictions = torch.cat(predictions)   #  predictions = torch.cat(predictions).cpu()
            # # if trainer.world_size > 1:
            # #     # print(f'Predictions returned: {len(all_predictions)}')
            # #     ddp_max_mem = torch.cuda.max_memory_allocated(trainer.local_rank) / 1000
            # #     logger.info(f"GPU {trainer.local_rank} max memory using DDP: {ddp_max_mem:.2f} MB")
            # #     gathered = [None] * torch.distributed.get_world_size()
            # #     torch.distributed.all_gather_object(gathered, predictions)
            # #     torch.distributed.all_gather_object(gathered, pred_batch_idx)
            # #     torch.distributed.barrier()
            # #     if not trainer.is_global_zero:
            # #         return
            # #     predictions = sum(gathered, [])
            # #     if trainer.global_rank == 0:
            # #         logger.info(f"All predictions gathered: {len(predictions)}")
            #
            # logger.info(f'Predictions returned: {len(predictions)}, writing to .h5 files ...')
            # #for idx, mixid in enumerate(p_mixids):
            # for i in pred_batch_idx:    # note assumes batch 0:num_mix matches 0:num_mix in mixdb.mixtures
            #     # print(f'{idx}, {mixid}')
            #     output_name = join(output_dir, mixdb.mixtures[i].name)
            #     pdat = predictions[i].cpu().numpy()
            #     logger.debug(f'Writing predict shape {pdat.shape} to {output_name}')
            #     with h5py.File(output_name, 'a') as f:
            #         if 'predict' in f:
            #             del f['predict']
            #         f.create_dataset('predict', data=pdat)
            #
            #     if wavdbg:
            #         owav_base = splitext(output_name)[0]
            #         tmp = torch.complex(predictions[idx][..., :half], predictions[idx][..., half:]).permute(2, 1, 0)
            #         predwav, _ = itf.execute_all(tmp.squeeze().detach().numpy())
            #         write_wav(owav_base + ".wav", predwav.detach().numpy(), 16000)

        logger.info(f'Saved results to {output_dir}')
        return

        # if reset:
        #     # reset mode cycles through each file one at a time
        #     for mixid in mixids:
        #         feature, _ = mixdb.mixture_ft(mixid)
        #         if feature.shape[0] > 2500:
        #             print(f'Trimming input frames from {feature.shape[0]} to {2500},')
        #             feature = feature[0:2500,::]
        #         half = feature.shape[-1] // 2
        #         noisy_spec_cmplx = torch.complex(torch.tensor(feature[..., :half]),
        #                                          torch.tensor(feature[..., half:])).to(device)
        #         del feature
        #
        #         predict = _pad_and_predict(built_model=model, feature=noisy_spec_cmplx)
        #         del noisy_spec_cmplx
        #
        #         audio_est = torch_istft_olsa_hanns(predict, mixdb.it_config.N, mixdb.it_config.R).cpu()
        #         del predict
        #         output_name = join(output_dir, splitext(mixdb.mixtures[mixid].name)[0]+'.wav')
        #         print(f'Saving prediction to {output_name}')
        #         write_wav(name=output_name, audio=float_to_int16(audio_est.detach().numpy()).transpose())
        #
        #         torch.cuda.empty_cache()
        #
        #         # TBD .h5 predict file optional output file
        #         # output_name = join(output_dir, mixdb.mixtures[mixid].name)
        #         # with h5py.File(output_name, 'a') as f:
        #         #     if 'predict' in f:
        #         #         del f['predict']
        #         #     f.create_dataset(name='predict', data=predict)
        #
        # else:
        #     # Run all data at once using a data generator
        #     feature = KerasFromH5(mixdb=mixdb,
        #                           mixids=mixids,
        #                           batch_size=hypermodel.batch_size,
        #                           timesteps=hypermodel.timesteps,
        #                           flatten=hypermodel.flatten,
        #                           add1ch=hypermodel.add1ch)
        #
        #     predict = built_model.predict(feature, batch_size=hypermodel.batch_size, verbose=1)
        #     predict, _ = reshape_outputs(predict=predict, timesteps=hypermodel.timesteps)
        #
        #     # Write data to separate files
        #     for idx, mixid in enumerate(mixids):
        #         output_name = join(output_dir, mixdb.mixtures[mixid].name)
        #         with h5py.File(output_name, 'a') as f:
        #             if 'predict' in f:
        #                 del f['predict']
        #             f.create_dataset('predict', data=predict[feature.file_indices[idx]])
        #
        # logger.info(f'Saved results to {output_dir}')
        # return

    logger.info(f'Run prediction on {len(datapaths):,} audio files')
    for file in datapaths:
        # Convert audio to feature data
        audio_in = read_audio(file)
        feature = get_feature_from_audio(audio=audio_in, feature_mode=model.hparams.feature)

        with torch.no_grad():
            predict = model(torch.tensor(feature))

        audio_out = get_audio_from_feature(feature=predict.numpy(), feature_mode=model.hparams.feature)

        output_name = join(output_dir, splitext(basename(file))[0] + '.h5')
        with h5py.File(output_name, 'a') as f:
            if 'audio_in' in f:
                del f['audio_in']
            f.create_dataset(name='audio_in', data=audio_in)

            if 'feature' in f:
                del f['feature']
            f.create_dataset(name='feature', data=feature)

            if 'predict' in f:
                del f['predict']
            f.create_dataset(name='predict', data=predict)

            if 'audio_out' in f:
                del f['audio_out']
            f.create_dataset(name='audio_out', data=audio_out)

        output_name = join(output_dir, splitext(basename(file))[0] + '_predict.wav')
        write_wav(output_name, audio_out, 16000)

    logger.info(f'Saved results to {output_dir}')
    del model


def _pad_and_predict(built_model: Any, feature: Feature) -> torch.Tensor:
    """
    Run prediction on feature [frames,1,bins*2] (stacked complex numpy array, stride/tsteps=1)
    Returns predict output [batch,frames,bins] in complex torch.tensor
    """
    noisy_spec = power_compress(torch.view_as_real(torch.from_numpy(feature).permute(1, 0, 2)))
    # print(f'noisy_spec type {type(noisy_spec_cmplx)}')
    # print(f'noisy_spec dtype {noisy_spec_cmplx.dtype}')
    # print(f'noisy_spec size {noisy_spec_cmplx.shape}')
    with torch.no_grad():
        est_real, est_imag = built_model(noisy_spec)  # expects in size [batch, 2, tsteps, bins]
    est_real, est_imag = est_real.permute(0, 1, 3, 2), est_imag.permute(0, 1, 3, 2)
    est_spec_uncompress = torch.view_as_complex(power_uncompress(est_real, est_imag).squeeze(1))
    # inv tf want [ch,frames,bins] complex (synonymous with [batch,tsteps,bins]), keep as torch.tensor
    predict = est_spec_uncompress.permute(0, 2, 1)  # .detach().numpy()

    return predict


if __name__ == '__main__':
    main()
