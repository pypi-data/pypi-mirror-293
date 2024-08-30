import random
from copy import deepcopy
from itertools import cycle
from typing import Optional

import numpy as np
from sonusai.mixture import GeneralizedIDs
from sonusai.mixture import MixtureDatabase
from sonusai.utils import reshape_inputs
from torch.utils.data import Dataset
from torch.utils.data import Sampler

from .dataloader_utils import AawareDataLoader
from .dataloader_utils import collate_fn


class MixIDPerSpeaker:
    def __init__(self, random_utterance: bool) -> None:
        self._random_utterance = random_utterance
        self._data: list[cycle] = []

    def append(self, mixids: list[int]) -> None:
        if self._random_utterance:
            self._data.append(cycle(random.sample(mixids, k=len(mixids))))
        else:
            self._data.append(cycle(mixids))

    def next(self, speaker_id: int) -> int:
        return next(self._data[speaker_id])


class MixtureDatabaseDataset(Dataset):
    """Generates a PyTorch dataset ordered by speaker ID and utterances from a SonusAI mixture database
    """

    def __init__(self,
                 mixdb: MixtureDatabase,
                 mixids: GeneralizedIDs,
                 speakers: int,
                 utterances: int,
                 cut_len: int,
                 flatten: bool,
                 add1ch: bool,
                 random_cut: bool = True,
                 random_utterance: bool = False):
        """Initialization
        """
        self.mixdb = mixdb
        self.mixids = self.mixdb.mixids_to_list(mixids)
        self.cut_len = cut_len
        self.flatten = flatten
        self.add1ch = add1ch
        self.random_cut = random_cut
        self.dataset_ids: list[int] = []

        # Get a list of IDs per speaker
        mixid_per_speaker = MixIDPerSpeaker(random_utterance)
        speaker_ids = mixdb.speech_metadata('speaker_id')
        for speaker_id in speaker_ids:
            data = mixdb.mixids_for_speech_metadata('speaker_id', speaker_id)
            mixid_per_speaker.append(data)
        speaker_indices = cycle(range(len(speaker_ids)))

        # Loop over speakers picking utterances per iteration
        # M utterances of Speaker0, M utterances of Speaker1, ...
        # Keep looping until all mixids have been used
        # This results in a new set of dataset indices that map into the original mixdb mixids
        unused_mixids = deepcopy(self.mixids)
        while unused_mixids:
            for _ in range(speakers):
                speaker = next(speaker_indices)
                for _ in range(utterances):
                    mixid = mixid_per_speaker.next(speaker)
                    self.dataset_ids.append(mixid)
                    try:
                        unused_mixids.remove(mixid)
                    except ValueError:
                        pass

    def __len__(self):
        return len(self.dataset_ids)

    def __getitem__(self, idx: int) -> tuple[np.ndarray, np.ndarray, int]:
        """Get data from one mixture
        """
        mixid = self.mixids[self.dataset_ids[idx]]
        feature, truth = self.mixdb.mixture_ft(mixid)
        feature, truth = reshape_inputs(feature=feature,
                                        truth=truth,
                                        batch_size=1,
                                        timesteps=0,
                                        flatten=self.flatten,
                                        add1ch=self.add1ch)

        length = feature.shape[0]

        if self.cut_len > 0:
            if length < self.cut_len:
                feature_final = []
                truth_final = []
                for _ in range(self.cut_len // length):
                    feature_final.append(feature)
                    truth_final.append(truth)
                feature_final.append(feature[: self.cut_len % length])
                truth_final.append(truth[: self.cut_len % length])
                feature = np.vstack([feature_final[i] for i in range(len(feature_final))])
                truth = np.vstack([truth_final[i] for i in range(len(truth_final))])
            else:
                if self.random_cut:
                    start = random.randint(0, length - self.cut_len)
                else:
                    start = 0
                feature = feature[start:start + self.cut_len]
                truth = truth[start:start + self.cut_len]

        return feature, truth, mixid


def TorchFromSpeakerIDMixtureDatabase(mixdb: MixtureDatabase,
                                      mixids: GeneralizedIDs,
                                      speakers: int,
                                      utterances: int,
                                      flatten: bool,
                                      add1ch: bool,
                                      num_workers: int = 0,
                                      cut_len: int = 0,
                                      drop_last: bool = False,
                                      shuffle: bool = False,
                                      random_cut: bool = True,
                                      random_utterance: bool = False,
                                      sampler: Optional[type[Sampler]] = None,
                                      pin_memory: bool = False) -> AawareDataLoader:
    """Generates a PyTorch dataloader from a SonusAI mixture database
    """
    dataset = MixtureDatabaseDataset(mixdb=mixdb,
                                     mixids=mixids,
                                     speakers=speakers,
                                     utterances=utterances,
                                     cut_len=cut_len,
                                     flatten=flatten,
                                     add1ch=add1ch,
                                     random_cut=random_cut,
                                     random_utterance=random_utterance)

    if sampler is not None:
        my_sampler = sampler(dataset)
    else:
        my_sampler = None

    batch_size = speakers * utterances

    if cut_len == 0 and batch_size > 1:
        result = AawareDataLoader(dataset=dataset,
                                  batch_size=batch_size,
                                  pin_memory=pin_memory,
                                  shuffle=shuffle,
                                  sampler=my_sampler,
                                  drop_last=drop_last,
                                  num_workers=num_workers,
                                  collate_fn=collate_fn)
    else:
        result = AawareDataLoader(dataset=dataset,
                                  batch_size=batch_size,
                                  pin_memory=pin_memory,
                                  shuffle=shuffle,
                                  sampler=my_sampler,
                                  drop_last=drop_last,
                                  num_workers=num_workers)

    result.cut_len = cut_len

    return result
