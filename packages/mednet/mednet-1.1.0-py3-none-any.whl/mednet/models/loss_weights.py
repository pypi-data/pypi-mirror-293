# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Methods to compute loss-weights for samples based on their classes."""

import logging
import typing

import numpy.typing
import torch
import torch.utils.data

from .typing import TargetType, TaskType

logger = logging.getLogger(__name__)


def _compute_multiclass_weights(targets: torch.Tensor) -> torch.Tensor:
    """Compute the positive weights when using exclusive, binary or multiclass
    targets.

    This function requires targets are one-hot-encoded.

    Parameters
    ----------
        targets
            A [n x C] tensor of integer values, where ``C`` is the number of
            target classes and ``n`` the number of samples.

    Returns
    -------
        The positive weights per class.
    """

    positive_count = targets.sum(dim=0)
    negative_count = torch.full((targets.shape[1],), float(targets.shape[0]))
    negative_count -= positive_count

    return negative_count / positive_count


def task_and_target_type(
    targets: torch.Tensor
    | numpy.typing.NDArray
    | typing.Iterable[typing.Iterable[int]]
    | typing.Iterable[typing.Iterable[typing.Iterable[typing.Iterable[int]]]],
) -> tuple[TaskType, TargetType]:
    """Determine the type of task from combined targets available.

    This function will look into the provided targets of a dataset and will
    determine the sought classifier or segmenter type.

    Parameters
    ----------
    targets
        The complete target set, for the whole dataset being analyzed. This
        matrix should be ``[n, C]`` where ``n`` is the number of samples, and
        ``C`` the number of classes.  All values should be either 0 or 1.

    Returns
    -------
        The type of task and targets available.
    """

    int_targets = torch.Tensor(targets).int()

    task_type: TaskType = "classification"
    if len(int_targets.shape) > 2:
        task_type = "segmentation"

    target_type: TargetType = "binary"
    if int_targets.shape[1] == 1:
        target_type = "binary"

    elif (int_targets.sum(dim=1) == 1).all().item():
        target_type = "multiclass"

    else:
        target_type = "multilabel"

    return task_type, target_type


def get_positive_weights(
    dataloader: torch.utils.data.DataLoader,
) -> torch.Tensor:
    """Compute the weights of each class of a DataLoader.

    This function inputs a pytorch DataLoader and computes the ratio between
    number of negative and positive samples (scalar).  The weight can be used
    to adjust minimisation criteria to in cases there is a huge data imbalance.

    It returns a vector with weights (inverse counts) for each target.

    Parameters
    ----------
    dataloader
        A DataLoader from which to compute the positive weights.  Entries must
        be a dictionary which must contain a ``target`` key.

    Returns
    -------
        The positive weight of each class in the dataset given as input.

    Raises
    ------
    NotImplementedError
        In the case of "multilabel" datasets, which are currently not
        supported.
    """

    targets = torch.vstack([batch["target"] for batch in dataloader])

    task_type, target_type = task_and_target_type(targets)

    if task_type == "segmentation":
        # rearranges ``targets`` vector so the problem looks like a simpler
        # classification problem where each pixel is a "separate sample"
        targets = targets.transpose(0, 2).transpose(1, 3).reshape(-1, targets.shape[1])

    match target_type:
        case "binary" | "multiclass":
            logger.info(f"Computing positive weights assuming {target_type} targets.")
            return _compute_multiclass_weights(targets)
        case "multilabel":
            raise NotImplementedError(
                f"Computing weights of {target_type} targets is not yet supported."
            )
