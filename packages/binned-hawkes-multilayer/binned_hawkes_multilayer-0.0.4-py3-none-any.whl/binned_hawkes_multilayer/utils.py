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
"""

from typing import List

import numpy as np
from nptyping import NDArray


def assert_sorted_node_list(node_list: List[str]):
    assert '<sep>'.join(node_list) == '<sep>'.join(
        sorted(node_list)), 'sorted_node_list was not sorted!'


def restore_nan_placeholder_params(params: NDArray, like: NDArray) -> NDArray:
    params = np.copy(params)
    for i in np.flatnonzero(np.isnan(like)):
        params = np.insert(params, i, np.nan)
    return params


def clobber_not_nan(template: NDArray, replacement: NDArray) -> NDArray:
    """For any not nan value in `template`, replace it with what is in `replacement` if it is not 0.

    Template may be longer than replacement, in which case the excess is retained.
    """
    result = np.array(template, copy=True, dtype='float')
    for i in range(len(replacement)):
        if not np.isnan(template[i]) and replacement[i] != 0:
            result[i] = replacement[i]
    return result
