"""
Copyright 2024 Matthew Sit

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Description: Utilities to perform discrete Residual Analysis.
"""

import matplotlib.pyplot as plt
import numpy as np
from nptyping import NDArray
from scipy import stats


def binned_to_continuous(Yt: NDArray, burn_in: int = 0):
    """Draws event times uniformly within each bin to create a continuous surrogate.

    Following Gerhard and Gerstner (2010): https://arxiv.org/abs/1011.4188.

    Args:
        Yt: Yt for one node.
        burn_in: Units of time of data from the beginning to discard.
    """
    result = []
    for i, val in enumerate(Yt):
        if i < burn_in:
            continue

        result.append(np.sort(np.random.uniform(
            low=i, high=i+1, size=int(val))))

    return np.concatenate(result)


def pvals(cont_Yt: NDArray, lmda: NDArray) -> NDArray:
    """Computes the upper-tail p-values of the compensator transformed event times.

    Args:
        cont_Yt: Output from `binned_to_continuous`; continuous surrogate representing one node.
        lmda: CIF for each unit of time, for one node.

    Returns:
        [p_ik for k in each index in cont_Yt], with node i being that of the single cont_Yt passed in.
    """
    # Lambda(t_k) - Lambda(t_{k-1})
    interarrival_time = []

    km1_time_unit, km1_within_time_unit = 0, 0  # for k - 1
    for k in range(len(cont_Yt)):
        k_time_unit, k_within_time_unit = int(
            cont_Yt[k]), cont_Yt[k] % 1  # for k

        interarrival_time.append(
            -lmda[km1_time_unit]*(km1_within_time_unit) +
            # upper-bound exclusive in Python
            np.sum(lmda[km1_time_unit:k_time_unit]) +
            lmda[k_time_unit]*k_within_time_unit)

        km1_time_unit, km1_within_time_unit = k_time_unit, k_within_time_unit

    return np.exp(-np.array(interarrival_time))


def kstest(pvals: NDArray) -> float:
    """Performs the KS test.

    Args:
        pvals: Output of `pvals()`.
    """
    return stats.kstest(pvals, stats.uniform.cdf).statistic


def visualize_continuous(cont_Yt: NDArray):
    """Scatter plot to visualize continuous surrogate Yt.

    Args:
        cont_Yt: Output from `binned_to_continuous`; continuous surrogate representing one node.
    """
    plt.scatter(cont_Yt, np.random.uniform(size=cont_Yt.shape))
    plt.show(block=False)


def visualize_pval_hist(pvals: NDArray):
    """Histogram of pvals.

    Args:
        pvals: Output of pvals.
    """
    plt.hist(pvals)
    plt.show(block=False)
