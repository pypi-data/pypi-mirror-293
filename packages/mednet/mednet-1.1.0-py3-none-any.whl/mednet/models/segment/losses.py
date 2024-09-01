# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Specialized losses for semanatic segmentation."""

import torch


class BCEWithLogitsLossWeightedPerBatch(torch.nn.Module):
    """Calculates the binary cross entropy loss for every batch.

    This loss is similar to :py:class:`torch.nn.BCEWithLogitsLoss`, except it
    updates the ``pos_weight`` (ratio between negative and positive target
    pixels) parameter for the loss term for every batch, based on the
    accumulated taget pixels for all samples in the batch.

    Implements Equation 1 in [MANINIS-2016]_.  The weight depends on the
    current proportion between negatives and positives in the ground-
    truth sample being analyzed.
    """

    def __init__(self):
        super().__init__()

    def forward(self, input_: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        """Forward pass.

        Parameters
        ----------
        input_
            Logits produced by the model to be evaluated, with the shape ``[n, c,
            h, w]``.
        target
            Ground-truth information with the shape ``[n, c, h, w]``,
            containing zeroes and ones.

        Returns
        -------
            The average loss for all input data.
        """

        # calculates the proportion of negatives to the total number of pixels
        # available in the masked region
        num_pos = target.sum()
        return torch.nn.functional.binary_cross_entropy_with_logits(
            input_,
            target,
            reduction="mean",
            pos_weight=(input_.numel() - num_pos) / num_pos,
        )


class SoftJaccardAndBCEWithLogitsLoss(torch.nn.Module):
    r"""Implement the generalized loss function of Equation (3) at [IGLOVIKOV-2018]_.

    At the paper, authors suggest a value of :math:`\alpha = 0.7`, which we set
    as default for instances of this type.

    .. math::

       L = \alpha H + (1-\alpha)(1-J)

    J is the Jaccard distance, and H, the Binary Cross-Entropy Loss.  Our
    implementation is based on :py:class:`torch.nn.BCEWithLogitsLoss`.

    Parameters
    ----------
    alpha
        Determines the weighting of J and H. Default: ``0.7``.
    """

    def __init__(self, alpha: float = 0.7):
        super().__init__()
        self.alpha = alpha

    def forward(self, input_: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        """Forward pass.

        Parameters
        ----------
        input_
            Logits produced by the model to be evaluated, with the shape ``[n, c,
            h, w]``.
        target
            Ground-truth information with the shape ``[n, c, h, w]``,
            containing zeroes and ones.

        Returns
        -------
            Loss, in a single entry.
        """

        eps = 1e-8
        probabilities = torch.sigmoid(input_)
        intersection = (probabilities * target).sum()
        sums = probabilities.sum() + target.sum()
        j = intersection / (sums - intersection + eps)

        # this implements the support for looking just into the RoI
        h = torch.nn.functional.binary_cross_entropy_with_logits(
            input_, target, reduction="mean"
        )
        return (self.alpha * h) + ((1 - self.alpha) * (1 - j))


class MultiLayerBCELogitsLossWeightedPerBatch(BCEWithLogitsLossWeightedPerBatch):
    """Weighted Binary Cross-Entropy Loss for multi-layered inputs.

    This loss can be used in networks that produce more than one output that
    has to match output targets.  For example, architectures such as
    as :py:class:`.hed.HED` or :py:class:`.lwnet.LittleWNet` require this
    feature.

    It follows the inherited super class applying on-the-fly `pos_weight`
    updates per batch.
    """

    def __init__(self):
        super().__init__()

    def forward(self, input_: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        """Forward pass.

        Parameters
        ----------
        input_
            Value produced by the model to be evaluated, with the shape ``[L,
            n, c, h, w]``.
        target
            Ground-truth information with the shape ``[n, c, h, w]``.

        Returns
        -------
            The average loss for all input data.
        """

        fwd = super().forward
        return torch.cat([fwd(i, target).unsqueeze(0) for i in input_]).mean()


class MultiLayerSoftJaccardAndBCELogitsLoss(SoftJaccardAndBCEWithLogitsLoss):
    """Implement Equation 3 in [IGLOVIKOV-2018]_ for the multi-output networks.

    This loss can be used in networks that produce more than one output that
    has to match output targets.  For example, architectures such as
    as :py:class:`.hed.HED` or :py:class:`.lwnet.LittleWNet` require this
    feature.

    Parameters
    ----------
    alpha : float
        Determines the weighting of SoftJaccard and BCE. Default: ``0.7``.
    """

    def __init__(self, alpha: float = 0.7):
        super().__init__(alpha=alpha)

    def forward(self, input_: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        """Forward pass.

        Parameters
        ----------
        input_
            Value produced by the model to be evaluated, with the shape ``[L,
            n, c, h, w]``.
        target
            Ground-truth information with the shape ``[n, c, h, w]``.

        Returns
        -------
            The average loss for all input data.
        """

        fwd = super().forward
        return torch.cat([fwd(i, target).unsqueeze(0) for i in input_]).mean()
