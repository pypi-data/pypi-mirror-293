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

Description: Unit tests for `ks.py`.
"""

import unittest

import numpy as np

import binned_hawkes_multilayer.residual_analysis as residual_analysis


class KSTest(unittest.TestCase):

    def test_binned_to_continuous(self):
        cont_Yts = residual_analysis.binned_to_continuous(
            np.array([1, 2, 5, 0, 3]))
        np.testing.assert_array_equal(
            cont_Yts.astype(int),
            np.array([0, 1, 1, 2, 2, 2, 2, 2, 4, 4, 4])
        )
        # Ensure sorted
        np.testing.assert_array_equal(cont_Yts, np.sort(cont_Yts))

    def test_binned_to_continuous_burn_in(self):
        cont_Yts = residual_analysis.binned_to_continuous(
            np.array([1, 2, 5, 0, 3]), burn_in=2)
        np.testing.assert_array_equal(
            cont_Yts.astype(int),
            np.array([2, 2, 2, 2, 2, 4, 4, 4])
        )
        # Ensure sorted
        np.testing.assert_array_equal(cont_Yts, np.sort(cont_Yts))

    def test_pvals_first_with_gap(self):
        np.testing.assert_almost_equal(
            residual_analysis.compute_pvals(
                cont_Yt=np.array([1.25]),
                lmda=np.array([5, 10])),
            np.array([np.exp(-(5*1+10*0.25))]))

    def test_pvals_first_on_hour(self):
        np.testing.assert_almost_equal(
            residual_analysis.compute_pvals(
                cont_Yt=np.array([0]),
                lmda=np.array([5])),
            np.array([np.exp(0)]))
        np.testing.assert_almost_equal(
            residual_analysis.compute_pvals(
                cont_Yt=np.array([1.0]),
                lmda=np.array([5, 10])),
            np.array([np.exp(-(5*1+10*0))]))

    def test_pvals_diff_across_same_hour(self):
        np.testing.assert_almost_equal(
            residual_analysis.compute_pvals(
                cont_Yt=np.array([0.25, 0.75]),
                lmda=np.array([5])),
            np.array([np.exp(-(5*0.25)), np.exp(-(5*0.5))]))

    def test_pvals_diff_across_same_hour_on_hour(self):
        np.testing.assert_almost_equal(
            residual_analysis.compute_pvals(
                cont_Yt=np.array([0.25, 1.0, 1.75]),
                lmda=np.array([5, 10])),
            np.array([np.exp(-(5*0.25)), np.exp(-(5*0.75+10*0)), np.exp(-(10*.75))]))

    def test_pvals_diff_across_different_hour(self):
        np.testing.assert_almost_equal(
            residual_analysis.compute_pvals(
                cont_Yt=np.array([0.25, 1.1]),
                lmda=np.array([5, 10])),
            np.array([np.exp(-(5*0.25)), np.exp(-(5*0.75+10*.1))]))

    def test_pvals_diff_across_different_hour_with_gap(self):
        np.testing.assert_almost_equal(
            residual_analysis.compute_pvals(
                cont_Yt=np.array([0.25, 2.1]),
                lmda=np.array([5, 10, 20])),
            np.array([np.exp(-(5*0.25)), np.exp(-(5*0.75+10*1+20*.1))]))

    def test_pvals_diff_across_different_hour_with_gap_on_hour(self):
        np.testing.assert_almost_equal(
            residual_analysis.compute_pvals(
                cont_Yt=np.array([0.25, 1.0, 3.0, 4.75, 6.0]),
                lmda=np.array([5, 10, 15, 20, 25, 30, 35])),
            np.array([
                np.exp(-(5*0.25)),
                np.exp(-(5*0.75)),
                np.exp(-(10+15)),
                np.exp(-(20+25*0.75)),
                np.exp(-(25*0.25+30)),
            ]))


if __name__ == '__main__':
    unittest.main()
