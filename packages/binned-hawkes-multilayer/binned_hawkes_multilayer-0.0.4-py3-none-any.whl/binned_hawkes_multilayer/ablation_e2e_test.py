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

Description: Unit tests for `ablation_e2e.py`.
"""

import unittest

import numpy as np
from nptyping import NDArray
from parameterized import parameterized

import data
from data import prep
import metadata
from metadata.station_graph import Region
from binned_hawkes_multilayer.ablation import ABLATION_MODELS

TEST_STATION = 'FTVL'
TEST_REGION = Region.PENINSULA


class AblationE2ETest(unittest.TestCase):
    """End to end change detector test for all abalation models.

    Run pytest in parallel using:
    pytest -n 4 .
    """

    def setUp(self):
        df = data.prep.load_data(2024, 'data')
        # These are consecutive stations that happen to be in alphabetical order.
        # (i.e. Fruitvale (FTVL) is between Coliseum (COLS) and Lake Merritt (LAKE).)
        self.reduced_stations = ['COLS', 'FTVL', 'LAKE', 'WOAK']
        _, df = data.prep.train_test_data_split(
            df, (2024, 1, 22), self.reduced_stations)
        train_df, _ = data.prep.train_test_data_split(
            df, (2024, 4, 1), self.reduced_stations)
        self.node_Yts = prep.get_node_Yts(
            df=train_df.copy(), sorted_node_list=self.reduced_stations, layer=TEST_REGION)
        self.layer_Yts = prep.get_layer_Yts(
            df=train_df.copy(), node=TEST_STATION, LayerEnum=Region)

    @parameterized.expand([
        [0, np.array([
            6.0651590e-02, 9.2170385e-01,
            1.0000000e-09, 2.0256475e-01, 1.0000000e-09, np.nan,
            1.0000000e-09, 9.9997469e-10, np.nan, 1.0000079e-09,
            2.5654985e-01, 5.3500345e-01,
        ])],
        [1, np.array([
            6.0655478e-02,
            9.2170495e-01,
            1.0000222e-09, 2.0256363e-01, 1.0000000e-09, np.nan,
            np.nan, np.nan, np.nan, np.nan,
            2.5654810e-01, 5.3500270e-01,
        ])],
        [2, np.array([
            7.2012739e-01,
            8.7724086e-01,
            1.0000000e-09, 8.7068518e-01, 1.0000001e-09, np.nan,
            9.9999704e-10, 9.9999893e-10, np.nan, 1.0000066e-09,
        ])],
        [3, np.array([
            6.0657011e-02,
            9.2170605e-01,
            np.nan, 2.0256388e-01, np.nan, np.nan,
            1.0001266e-09, 1.0000000e-09, np.nan, 1.0000647e-09,
            2.5654792e-01, 5.3499900e-01,
        ])],
        [4, np.array([
            7.2012696e-01,
            8.7724055e-01,
            1.0000000e-09, 8.7068510e-01, 1.0000000e-09, np.nan,
            np.nan, np.nan, np.nan, np.nan,
        ])],
        [5, np.array([
            0.0606563,
            0.9217057,
            np.nan, 0.2025636, np.nan, np.nan,
            np.nan, np.nan, np.nan, np.nan,
            0.2565479, 0.5350004,
        ])],
        [6, np.array([
            7.2012719e-01,
            8.7724052e-01,
            np.nan, 8.7068486e-01, np.nan, np.nan,
            9.9999631e-10, 9.9999960e-10, np.nan, 1.0000006e-09,
        ])],
        [7, np.array([
            0.7201269,
            0.8772408,
            np.nan, 0.8706853, np.nan, np.nan,
            np.nan, np.nan, np.nan, np.nan,
        ])],
        [8, np.array([
            5.5607142,
            0.95,
            np.nan, np.nan, np.nan, np.nan,
            np.nan, np.nan, np.nan, np.nan,
        ])],
    ])
    def test_fit(self, abalation_num: int, expected_params: NDArray):
        np.random.seed(0)
        m = ABLATION_MODELS[abalation_num](
            node=TEST_STATION, layer=TEST_REGION)
        m.fit(node_Yts=self.node_Yts,
              layer_Yts=self.layer_Yts,
              sorted_node_list=self.reduced_stations,
              intralayer_network=metadata.station_graph.get(),
              enable_basinhopping=False)
        np.testing.assert_almost_equal(m.params, expected_params, decimal=3)
