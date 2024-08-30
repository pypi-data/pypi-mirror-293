import torch


class TorchLInverseTransform:
    def __init__(self,
                 N: int = 256,
                 R: int = 64,
                 bin_start: int = 0,
                 bin_end: int = 128,
                 ttype: str = 'stft-olsa-hanns',
                 gain: float = 1,
                 device=torch.device('cpu')) -> None:
        from pyaaware.transform_types import Overlap
        from pyaaware.transform_types import Window
        from pyaaware.transform_types import window

        # logger.debug(f"SonusAI TorchLInverse init device: '{device}'")
        # Note: no need to set device since init is always on cpu, see execute()
        self._device = device
        self._N = N  # torch.tensor(N).to(device)
        self._R = R  # torch.tensor(R).to(device)
        self._bin_start = bin_start  # torch.tensor(bin_start).to(device)
        self._bin_end = bin_end  # torch.tensor(bin_end).to(device)
        self._ttype = ttype
        self._gain = gain  # torch.tensor(gain).to(device)

        if self.N % self.R:
            raise ValueError('R is not a factor of N')

        if self.bin_start > self.N // 2:
            raise ValueError('bin_start is greater than N//2')

        if self.bin_end > self.N // 2:
            raise ValueError('bin_end is greater than N//2')

        if self.bin_start >= self.bin_end:
            raise ValueError('bin_start is greater than bin_end')

        self._bins = self.bin_end - self.bin_start + 1

        self._bin_indices = list(range(self.bin_start, self.bin_end + 1))

        # calc if some bins are zero (feature transform is not full bin)
        self._zero_bin_mode = self.bin_start > 0 or self.bin_end < self.N // 2

        self._W = None
        self._overlap_type = None

        if self.ttype == 'stft-olsa-hanns':
            self._W = window(Window.HANN01, self.N, self.R)
            itr_user_gain = self.N / 2
            self._overlap_type = Overlap.OLA
        elif self.ttype == 'stft-ols':
            self._W = window(Window.NONE, self.N, self.R)
            itr_user_gain = self.N ** 2 / self.R / 2
            self._overlap_type = Overlap.OLS
        elif self.ttype == 'stft-olsa':
            self._W = window(Window.W01, self.N, self.R)
            itr_user_gain = self.N / 2
            self._overlap_type = Overlap.OLA
        elif self.ttype == 'stft-olsa-hann':
            self._W = window(Window.NONE, self.N, self.R)
            itr_user_gain = self.N / 2
            self._overlap_type = Overlap.OLA
        elif self.ttype == 'stft-olsa-hannd':
            self._W = window(Window.HANN, self.N, self.R)
            itr_user_gain = self.N / 3
            self._overlap_type = Overlap.OLA
        elif self.ttype == 'stft-olsa-hammd':
            self._W = window(Window.HAMM, self.N, self.R)
            itr_user_gain = self.N / 2.72565243
            self._overlap_type = Overlap.OLA
        elif self.ttype == 'stft-ola':
            self._W = window(Window.NONE, self.N, self.R)
            itr_user_gain = self.N ** 2 / self.R / 2
            self._overlap_type = Overlap.OLA
        elif self.ttype in ('tdac', 'tdac-co'):
            self._R = self.N // 2
            self._real_mode = False

            k = torch.arange(1, self.R)
            self._W = torch.conj(torch.exp(-1j * 2 * torch.pi / 8 * (2 * k + 1)) * torch.exp(
                -1j * 2 * torch.pi / (2 * self.N) * k)) / 4
            itr_user_gain = 1

            if self.ttype == 'tdac':
                self._overlap_type = Overlap.TDAC
            else:
                self._overlap_type = Overlap.TDAC_CO
        else:
            raise ValueError(f"Unknown ttype: '{self.ttype}'")

        if self._overlap_type not in (Overlap.TDAC, Overlap.TDAC_CO):
            if len(self._W) != self.N:
                raise RuntimeError('W is not of length N')

            wdc_gain = torch.sum(self._W)
            o_gain = 1 / (self.gain * wdc_gain / self.R) * itr_user_gain
            self._W = self._W * o_gain

        self.fold_params = {
            'kernel_size': (self._N, 1),
            'stride':      (self._R, 1),
        }

    @property
    def device(self) -> torch.device:
        return self._device

    @property
    def N(self) -> int:
        return self._N

    @property
    def R(self) -> int:
        return self._R

    @property
    def bin_start(self) -> int:
        return self._bin_start

    @property
    def bin_end(self) -> int:
        return self._bin_end

    @property
    def ttype(self) -> str:
        return self._ttype

    @property
    def gain(self) -> float:
        return self._gain

    @property
    def bins(self) -> int:
        return self._bins

    @property
    def W(self) -> torch.Tensor:
        return self._W

    def execute_all(self, xf: torch.Tensor) -> torch.Tensor:
        """Run inverse transform with shapes: [batch, timesteps, bins] -> [batch, samples].
        """
        import torch
        from pyaaware.transform_types import Overlap
        from sonusai import logger

        if xf.ndim != 2 and xf.ndim != 3:
            raise ValueError('Input must have either 2 or 3 dimensions')

        bins = xf.shape[0]
        if bins != self.bins:
            raise ValueError(f'Input must have {self.bins} bins')

        if self._zero_bin_mode:
            logger.debug(f'TBD: SonusAI TorchLInverse zero pad for sub-bin mode')
            zero_tmp = torch.zeros((xf.shape[0], xf.shape[1], self.N // 2), dtype=xf.dtype)
            zero_tmp[..., self._bin_indices] = xf  # TBD, probably need to use clone to keep gradients correct
            xf = zero_tmp

        n_frames = xf.size(-2)
        print(f'N:        {self.N}')
        print(f'R:        {self.R}')
        print(f'ttype:    {self.ttype}')
        print(f'xf:       {xf.shape}')
        # have to check and move to device here because init is run on cpu
        if self.device != xf.device:
            self._device = xf.device
            self._W = self.W.to(self.device)
            # logger.debug(f"SonusAI TorchLInverse execute_all() vars move to device: '{self.device}'")

        if self._overlap_type == Overlap.OLA:
            xf.to(self.device)
            # TBD zero
            # yt = torch.fft.irfft(xf, dim=-1, norm='backward')
            yt = torch.fft.irfft(xf, dim=-1, n=self.N)
            print(f'yt:       {yt.shape}')
            print(f'W:        {self.W.shape}')
            print(f'W.view(): {self.W.view(1, 1, self.N).shape}')
            assert yt.size(-1) == self.N
            # multiple windows, tensor does expansion to [batch, timesteps, samples]
            yt = yt * self.W.view(1, 1, self.N)
            # Use nn.fold() to apply overlap-add, seems very fast, supported on gpu
            yt = yt.transpose(1, 2)
            print(f'yt:       {yt.shape}')
            expected_output_signal_len = self.N + self.R * (n_frames - 1)
            y = torch.nn.functional.fold(yt, output_size=(expected_output_signal_len, 1), **self.fold_params)
            print(f'yt:       {yt.shape}')
            y = y.reshape(y.size(0), -1)
            print(f'yt:       {yt.shape}')
            assert y.size(1) == expected_output_signal_len
            # always trim latency to match input
            y = y[..., self.N - self.R:self.R * n_frames]  # OLA trim
            print(f'yt:       {yt.shape}')
        else:
            raise ValueError(f"Unsupported overlap type: '{self._overlap_type}'")

        return y
