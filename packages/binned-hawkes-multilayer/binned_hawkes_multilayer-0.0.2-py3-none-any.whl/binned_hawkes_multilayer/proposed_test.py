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

Description: Unit tests for `proposed.py`.
"""

import datetime
import unittest

import numpy as np
import pandas as pd
from scipy.special import logit

import metadata
from metadata.station_graph import Region
from binned_hawkes_multilayer.proposed import ProposedModel


class ProposedModelTest(unittest.TestCase):

    def test_get_params_attribute(self):
        m = ProposedModel(
            node='EMBR', layer=Region.SAN_FRANCISCO, self_excite_time_shifts=[])
        m.sorted_node_list = ['EMBR', 'SBRN']
        m.params = np.arange(8)

        actual_baseline, actual_beta, actual_alpha_mutual, actual_alpha_layer, actual_alpha_shifted = m.get_params()
        self.assertEqual(actual_baseline, 0)
        self.assertEqual(actual_beta, 1)
        np.testing.assert_array_equal(actual_alpha_mutual, np.array([2, 3]))
        np.testing.assert_array_equal(
            actual_alpha_layer, np.array([4, 5, 6, 7]))
        np.testing.assert_array_equal(actual_alpha_shifted, np.array([]))

    def test_get_params_attribute_time_shifts(self):
        m = ProposedModel(
            node='EMBR', layer=Region.SAN_FRANCISCO, self_excite_time_shifts=[24, 168])
        m.sorted_node_list = ['EMBR', 'SBRN']
        m.params = np.arange(10)

        actual_baseline, actual_beta, actual_alpha_mutual, actual_alpha_layer, actual_alpha_shifted = m.get_params()
        self.assertEqual(actual_baseline, 0)
        self.assertEqual(actual_beta, 1)
        np.testing.assert_array_equal(actual_alpha_mutual, np.array([2, 3]))
        np.testing.assert_array_equal(
            actual_alpha_layer, np.array([4, 5, 6, 7]))
        np.testing.assert_array_equal(actual_alpha_shifted, np.array([8, 9]))

    def test_get_params_custom(self):
        m = ProposedModel(
            node='EMBR', layer=Region.SAN_FRANCISCO, self_excite_time_shifts=[])
        m.sorted_node_list = ['EMBR', 'SBRN']
        m.params = np.arange(8)

        actual_baseline, actual_beta, actual_alpha_mutual, actual_alpha_layer, actual_alpha_shifted = m.get_params(
            np.arange(10, 18))
        self.assertEqual(actual_baseline, 10)
        self.assertEqual(actual_beta, 11)
        np.testing.assert_array_equal(actual_alpha_mutual, np.array([12, 13]))
        np.testing.assert_array_equal(
            actual_alpha_layer, np.array([14, 15, 16, 17]))
        np.testing.assert_array_equal(actual_alpha_shifted, np.array([]))

    def test_get_params_custom_time_shifts(self):
        m = ProposedModel(
            node='EMBR', layer=Region.SAN_FRANCISCO, self_excite_time_shifts=[24, 168])
        m.sorted_node_list = ['EMBR', 'SBRN']
        m.params = np.arange(10)

        actual_baseline, actual_beta, actual_alpha_mutual, actual_alpha_layer, actual_alpha_shifted = m.get_params(
            np.arange(10, 20))
        self.assertEqual(actual_baseline, 10)
        self.assertEqual(actual_beta, 11)
        np.testing.assert_array_equal(actual_alpha_mutual, np.array([12, 13]))
        np.testing.assert_array_equal(
            actual_alpha_layer, np.array([14, 15, 16, 17]))
        np.testing.assert_array_equal(actual_alpha_shifted, np.array([18, 19]))

    def test_get_params_malformed(self):
        m = ProposedModel(
            node='EMBR', layer=Region.SAN_FRANCISCO, self_excite_time_shifts=[])
        m.sorted_node_list = ['EMBR', 'SBRN']
        m.params = np.arange(4)

        # too few
        with self.assertRaises(AssertionError):
            m.get_params(np.arange(3))

        # too many
        with self.assertRaises(AssertionError):
            m.get_params(np.arange(5))

    def test_get_params_malformed_time_shifts(self):
        m = ProposedModel(
            node='EMBR', layer=Region.SAN_FRANCISCO, self_excite_time_shifts=[24, 168])
        m.sorted_node_list = ['EMBR', 'SBRN']
        m.params = np.arange(4)

        # missing burn ins
        with self.assertRaises(AssertionError):
            m.get_params(np.arange(4))

        # too few
        with self.assertRaises(AssertionError):
            m.get_params(np.arange(5))

        # too many
        with self.assertRaises(AssertionError):
            m.get_params(np.arange(7))

    def test_init_params(self):
        m = ProposedModel(
            node='SFIA', layer=Region.SAN_FRANCISCO, regularization=1, self_excite_time_shifts=[])
        m.init_params(['EMBR', 'ORIN', 'SBRN', 'SFIA'], metadata.station_graph.get())
        self.assertIsNotNone(m.intralayer_network)
        self.assertEqual(m.sorted_node_list, ['EMBR', 'ORIN', 'SBRN', 'SFIA'])
        np.testing.assert_array_equal(
            m.params,
            np.array([
                1,
                0.95,
                np.nan, np.nan, 1e-9, 0.5,
                np.nan, 1e-9, 1e-9, 1e-9,
            ]))

        m = ProposedModel(
            node='SFIA', layer=Region.PENINSULA, regularization=np.inf, self_excite_time_shifts=[])
        m.init_params(['EMBR', 'ORIN', 'SBRN', 'SFIA'], metadata.station_graph.get())
        np.testing.assert_array_equal(
            m.params,
            np.array([
                1,
                0.95,
                1e-9, 1e-9, 1e-9, 0.5,
                1e-9, 1e-9, np.nan, 1e-9,
            ]))

        m = ProposedModel(
            node='SFIA', layer=Region.EAST_BAY, self_excite_time_shifts=[24, 168])
        m.init_params(['EMBR', 'ORIN', 'SBRN', 'SFIA'], metadata.station_graph.get())
        np.testing.assert_array_equal(
            m.params,
            np.array([
                1,
                0.95,
                np.nan, np.nan, 1e-9, 0.5,
                1e-9, 1e-9, 1e-9, np.nan,
                0.5, 0.5,
            ]))

        m = ProposedModel(
            node='SFIA', layer=Region.EAST_BAY, multilayer_excite=False, self_excite_time_shifts=[])
        m.init_params(['EMBR', 'ORIN', 'SBRN', 'SFIA'], metadata.station_graph.get())
        np.testing.assert_array_equal(
            m.params,
            np.array([
                1,
                0.95,
                np.nan, np.nan, 1e-9, 0.5,
                np.nan, np.nan, np.nan, np.nan,
            ]))

    def test_nll(self):
        m = ProposedModel(
            node='16TH', layer=Region.SAN_FRANCISCO, self_excite_time_shifts=[])
        # only '24TH' neighbors '16TH'
        m.sorted_node_list = ['12TH', '16TH', '19TH', '24TH', 'ORIN']
        m.params = np.array([
            1,
            1,
            np.nan, 0, np.nan, 0, np.nan,
            np.nan, 1, 1, 1,
        ])

        np.testing.assert_almost_equal(
            m._nll(np.array([
                np.log(10),
                logit(0.99),
                logit(0.94), logit(0.8),
                logit(0.1), logit(0.01), -np.inf,
            ]),
                [np.arange(200, 100, -1), np.arange(100),
                 np.arange(100), np.arange(100), np.arange(100)],
                [np.arange(100)]*4),
            -13770.677573647179)

    def test_pack_unpack_param_constraints(self):
        m = ProposedModel(
            node='16TH', layer=Region.SAN_FRANCISCO, self_excite_time_shifts=[])

        # Standard usage.
        m.params = np.array([25, 0.99, np.nan, 0.5, np.nan, 0.1, np.nan])
        np.testing.assert_array_almost_equal(
            m._pack_param_constraints(m.params), np.array([3.218876,  4.59512, 0, -2.197225]))
        np.testing.assert_array_almost_equal(
            m._unpack_param_constraints(
                # Perturb after packing to distinguish expected from m.params.
                m._pack_param_constraints(m.params)*2),
            np.array([625, 0.999898, np.nan, 0.5, np.nan, 0.01219512, np.nan]))

    def test_pack_unpack_param_constraints_shifted_self(self):
        m = ProposedModel(
            node='16TH', layer=Region.SAN_FRANCISCO, self_excite_time_shifts=[24, 168])
        m.sorted_node_list = ['16TH', '24TH']
        m.params = np.array(
            [25, 0.99, 0.1, 0.5, np.nan, 0.1, np.nan, 0.2, 0.3])
        self.assertEqual(m._pack_param_constraints(m.params)[-1], 0)
        # 0.1 + 0.2 + 0.3 + 0.5 (default dummy) ==> 1.1
        np.testing.assert_array_almost_equal(
            m._unpack_param_constraints(m._pack_param_constraints(m.params)),
            np.array([25, 0.99, 0.1/1.1, 0.5, np.nan, 0.1, np.nan, 0.2/1.1, 0.3/1.1]))

    def test_regularization_nan(self):
        m = ProposedModel(
            node='16TH', layer=Region.SAN_FRANCISCO, multilayer_excite=False, regularization=1, self_excite_time_shifts=[])
        df = pd.DataFrame({
            'timestamp': [
                datetime.datetime(2024, 1, 1, 0),
                datetime.datetime(2024, 1, 1, 0),
                datetime.datetime(2024, 1, 1, 0),
            ],
            'origin': ['24TH', '16TH', '16TH'],
            'dest': ['16TH', '24TH', 'SFIA'],
            'count': [1, 2, 3]})
        m.init_params(['16TH', '24TH', 'SFIA'], metadata.station_graph.get())
        np.testing.assert_array_equal(
            m.params,
            np.array([1, 0.95,
                      0.5, 1e-9, np.nan,
                      np.nan, np.nan, np.nan, np.nan]))

        m = ProposedModel(
            node='16TH', layer=Region.SAN_FRANCISCO, multilayer_excite=False, regularization=0, self_excite_time_shifts=[])
        m.init_params(['16TH', '24TH', 'SFIA'], metadata.station_graph.get())
        np.testing.assert_array_equal(
            m.params,
            np.array([1, 0.95,
                      0.5, np.nan, np.nan,
                      np.nan, np.nan, np.nan, np.nan]))

        m = ProposedModel(
            node='16TH', layer=Region.SAN_FRANCISCO, multilayer_excite=False, regularization=-1, self_excite_time_shifts=[])
        m.init_params(['16TH', '24TH', 'SFIA'], metadata.station_graph.get())
        np.testing.assert_array_equal(
            m.params,
            np.array([1, 0.95,
                      np.nan, np.nan, np.nan,
                      np.nan, np.nan, np.nan, np.nan]))

        m = ProposedModel(
            node='16TH', layer=Region.SAN_FRANCISCO, multilayer_excite=False, regularization=np.inf, self_excite_time_shifts=[])
        m.init_params(['16TH', '24TH', 'SFIA'], metadata.station_graph.get())
        np.testing.assert_array_equal(
            m.params,
            np.array([1, 0.95,
                      0.5, 1e-9, 1e-9,
                      np.nan, np.nan, np.nan, np.nan]))


if __name__ == '__main__':
    unittest.main()
