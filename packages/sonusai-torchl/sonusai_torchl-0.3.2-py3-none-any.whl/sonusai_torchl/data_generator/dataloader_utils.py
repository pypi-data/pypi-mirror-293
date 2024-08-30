from typing import Any
from typing import Optional

import numpy as np
import torch
from torch.utils.data import DataLoader


class AawareDataLoader(DataLoader):
    _cut_len: Optional[int] = None

    @property
    def cut_len(self) -> int:
        return self._cut_len

    @cut_len.setter
    def cut_len(self, value: int) -> None:
        self._cut_len = value


def collate_fn(data: list[tuple[np.ndarray, np.ndarray, int]]) -> list[tuple[np.ndarray, np.ndarray, int]]:
    """Use this collate function whenever cut_len == 0 and batch_size > 1.

    Pad mixtures with zeros so that they have the same length and can be concatenated.
    Once the features and truths have been padded to the same length, then call the default Torch collate function.
    """
    max_len = max(item[0].shape[0] for item in data)

    features_ndim = data[0][0].ndim
    features_pad_width = [(0, 0)] * features_ndim

    truths_ndim = data[0][1].ndim
    truths_pad_width = [(0, 0)] * truths_ndim

    new_data: list[tuple[np.ndarray, np.ndarray, int]] = []
    for n in range(len(data)):
        feature = data[n][0]
        truth = data[n][1]
        mixid = data[n][2]

        this_len = feature.shape[0]
        pad_len = max_len - this_len

        features_pad_width[0] = (0, pad_len)
        truths_pad_width[0] = (0, pad_len)

        new_data.append((
            np.pad(feature, list_to_tuple(features_pad_width), mode='constant', constant_values=0),
            np.pad(truth, list_to_tuple(truths_pad_width), mode='constant', constant_values=0),
            mixid
        ))

    return torch.utils.data.dataloader.default_collate(new_data)


def list_to_tuple(lst: list[Any]) -> tuple[Any, ...]:
    return tuple(tuple(x) for x in lst)
