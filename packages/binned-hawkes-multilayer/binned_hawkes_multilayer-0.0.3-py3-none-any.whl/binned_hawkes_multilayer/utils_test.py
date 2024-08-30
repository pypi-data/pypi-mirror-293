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

Description: Unit tests for `utils.py`.
"""

import unittest

import numpy as np

import binned_hawkes_multilayer.utils as utils


class UtilsTest(unittest.TestCase):

    def test_assert_sorted_node_list(self):
        utils.assert_sorted_node_list(['A', 'B', 'C'])
        with self.assertRaises(AssertionError):
            utils.assert_sorted_node_list(['D', 'A', 'B', 'C'])

    def test_restore_nan_placeholder_params(self):
        np.testing.assert_array_equal(
            utils.restore_nan_placeholder_params(
                params=np.arange(1, 7, dtype=float),
                like=np.array([1, 1, 1, 1, np.nan, np.nan, 1, np.nan, 1, np.nan, np.nan, np.nan])),
            np.array([1, 2, 3, 4, np.nan, np.nan, 5, np.nan, 6, np.nan, np.nan, np.nan]))

    def test_clobber_not_nan(self):
        np.testing.assert_equal(utils.clobber_not_nan(
            template=np.array([5, np.nan, 1, 2, np.nan,
                               # template may be longer
                               9, 9]),
            replacement=np.arange(5),
        ), np.array([
            5,  # zero does not get clobbered
            np.nan, 2, 3, np.nan,
            # extras from the template are retained
            9, 9,
        ]))

    def test_clobber_not_nan_ablation_mixed(self):
        replacement_ablation_4 = np.array([
            40, 0.4,
            0.4, 0.4, 0,
            0, 0, 0, 0,
        ])
        replacement_ablation_5 = np.array([
            55, 0.55,
            0.55, 0, 0,
            0, 0, 0, 0,
            0.55, 0.55,
        ])
        replacement_ablation_6 = np.array([
            60, 0.6,
            0.6, 0, 0,
            0.6, 0.6, 0.6, 0.6,
        ])

        # Ablation 1
        np.testing.assert_equal(
            utils.clobber_not_nan(
                utils.clobber_not_nan(
                    np.array([
                        1, 0.95,
                        0.5, 1e-9, np.nan,
                        np.nan, np.nan, np.nan, np.nan,
                        0.5, 0.5,
                    ]), replacement_ablation_4),
                replacement_ablation_5),
            np.array([
                55, 0.55,
                0.55, 0.4, np.nan,
                np.nan, np.nan, np.nan, np.nan,
                0.55, 0.55,
            ]))

        # Ablation 2
        np.testing.assert_equal(
            utils.clobber_not_nan(
                utils.clobber_not_nan(
                    np.array([
                        1, 0.95,
                        0.5, 1e-9, np.nan,
                        1e-9, 1e-9, 1e-9, 1e-9,
                    ]), replacement_ablation_4),
                replacement_ablation_6),
            np.array([
                60, 0.6,
                0.6, 0.4, np.nan,
                0.6, 0.6, 0.6, 0.6,
            ]))

        # Ablation 3
        np.testing.assert_equal(
            utils.clobber_not_nan(
                utils.clobber_not_nan(
                    np.array([
                        1, 0.95,
                        0.5, np.nan, np.nan,
                        1e-9, 1e-9, 1e-9, 1e-9,
                        0.5, 0.5,
                    ]), replacement_ablation_5),
                replacement_ablation_6),
            np.array([
                60, 0.6,
                0.6, np.nan, np.nan,
                0.6, 0.6, 0.6, 0.6,
                0.55, 0.55,
            ]))

        # Ablation 0
        np.testing.assert_equal(
            utils.clobber_not_nan(
                utils.clobber_not_nan(
                    utils.clobber_not_nan(
                        np.array([
                            1, 0.95,
                            0.5, 1e-9, np.nan,
                            1e-9, 1e-9, 1e-9, 1e-9,
                            0.5, 0.5,
                        ]), replacement_ablation_4),
                    replacement_ablation_5),
                replacement_ablation_6),
            np.array([
                60, 0.6,
                0.6, 0.4, np.nan,
                0.6, 0.6, 0.6, 0.6,
                0.55, 0.55,
            ]))


if __name__ == '__main__':
    unittest.main()
