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

import time
from enum import Enum
from typing import List, Optional, Tuple

import networkx as nx
import numpy as np
from nptyping import NDArray
from scipy.optimize import basinhopping
from scipy.special import expit, logit

import binned_hawkes_multilayer.utils as utils


class ProposedModel:
    """The proposed model.

    Args:
        node: Name of the node being fit.
        layer: Layer being fit.
        regularization: d-order neighborhood for regularized mutual excitement.
        self_excite_time_shifts: Set of shifts for shifted self excitement.
        multilayer_excite: Whether or not to use multilayer contextual excitement.
    """

    def __init__(self,
                 node: str,
                 layer: Enum,
                 regularization: int = 1,
                 self_excite_time_shifts: List[int] = [24, 168],
                 multilayer_excite: bool = True):
        self.node = node
        self.layer = layer

        self.regularization = regularization
        self.self_excite_time_shifts = self_excite_time_shifts
        self.multilayer_excite = multilayer_excite

        # initialized by init_params()
        self.sorted_node_list = []
        self.intralayer_network = None
        # baseline, beta, mutual excite alpha, multilayer excite alpha, shifted self excite alpha
        self.params = None

    def get_params(
            self, params: Optional[NDArray] = None) -> Tuple[float, float, NDArray, NDArray, NDArray]:
        """Gets the trained or custom params and formats the flat tuple into triplet.

        Args:
            params: Custom list of params.
                If None, uses the trained self.params.

        Returns:
            (baseline, beta, alpha mutual excite list, alpha multilayer excite list, alpha self excite list)
        """
        if params is None:
            params = self.params

        params = np.nan_to_num(params)

        # Baseline
        baseline = params[0]

        # Geometric decay factor
        beta = params[1]

        # (Regularized) mutual excitement
        alpha_mutual = params[2:2+len(self.sorted_node_list)]
        assert len(alpha_mutual) == len(self.sorted_node_list)

        # Multilayer contextual excitement
        alpha_layer = params[2+len(self.sorted_node_list):2+len(self.sorted_node_list)+len(type(self.layer))]
        assert len(alpha_layer) == len(type(self.layer))

        # Shifted self excitement
        alpha_shifted_self = params[2 +
                                    len(self.sorted_node_list)+len(type(self.layer)):]
        assert len(alpha_shifted_self) == len(self.self_excite_time_shifts)

        return baseline, beta, alpha_mutual, alpha_layer, alpha_shifted_self

    def pretty_print_params(self, ablation_num: Optional[int] = None):
        baseline, beta, alpha_mutual, alpha_layer, alpha_shifted_self = self.get_params()
        if ablation_num is not None:
            print('ablation model:', ablation_num, sep='\t')
        print('node:', self.node, sep='\t')
        print('layer:\t', self.layer, sep='\t')
        print()
        print('baseline', '=', baseline, sep='\t')
        print('beta', '=', beta, sep='\t')
        print()
        print('alpha_mutual', alpha_mutual, sep='\n')
        print()
        print('alpha_layer', alpha_layer, sep='\n')
        print()
        print('alpha_shifted_self', alpha_shifted_self, sep='\n')
        print()

    def _nll(self, params: NDArray, node_Yts: List[NDArray], layer_Yts: Optional[List[NDArray]] = None) -> float:
        """Negative log-likelihood.

        Args:
          params: (baseline, beta, alpha list)
          node_Yts: list of the event data for each node, same order as `self.sorted_node_list`.
          layer_Yts: list of the event data for each layer, same order as `Layer`.
        """
        params = self._unpack_param_constraints(params)

        lmda = self.lmda(node_Yts, layer_Yts, params)
        i = self.sorted_node_list.index(self.node)
        # sum over time
        return -np.sum((node_Yts[i] * np.log(lmda + 1e-9) - lmda)[max(self.self_excite_time_shifts + [0]):])

    def _get_R(self, Yt: NDArray, beta: float, time_shift: int = 1) -> NDArray:
        delta = len(Yt)
        R = np.zeros(delta)  # depends on history of events H_{t-1}
        for j in range(time_shift-1, delta-1):
            R[j+1] = (1-beta)*R[j] + Yt[j-time_shift+1]*beta
        return R

    def lmda(
            self, node_Yts: List[NDArray], layer_Yts: Optional[List[NDArray]] = None, params=None
    ) -> NDArray:
        """Conditional intensity function lambda.

        Args:
          node_Yts: list of the event data for each node, same order as `self.sorted_node_list`.
          layer_Yts: list of the event data for each layer, same order as `Layer`.
          params: (baseline, beta, alpha list)
        """
        baseline, beta, alpha_mutual, alpha_layer, alpha_shifted_self = self.get_params(
            params)

        i = self.sorted_node_list.index(self.node)
        result = baseline * np.ones(len(node_Yts[0]))
        # (regularized) mutual excitement
        for l in range(len(self.sorted_node_list)):
            if alpha_mutual[l] == 0:
                continue
            result += alpha_mutual[l] * self._get_R(node_Yts[l], beta)

        # shifted self excitement
        for j, time_shift in enumerate(self.self_excite_time_shifts):
            result += alpha_shifted_self[j] * \
                self._get_R(node_Yts[i], beta, time_shift)

        # multilayer contextual excitement
        if self.multilayer_excite:
            for r in range(len(type(self.layer))):
                if alpha_layer[r] == 0:
                    continue
                result += alpha_layer[r] * \
                    self._get_R(layer_Yts[r], beta)

        return result

    def init_params(self, sorted_node_list: List[str], intralayer_network: nx.Graph):
        """Initializes the parameters.

        Args:
            sorted_node_list: The graph's full vertex set as an alphabetized list.
            intralayer_network: The intralayer network structure.
        """
        utils.assert_sorted_node_list(sorted_node_list)
        self.sorted_node_list = sorted_node_list
        self.intralayer_network = intralayer_network

        self.params = np.array(
            # baseline
            [1] +
            # beta
            [0.95] +
            # alpha mutual excite
            [1e-9] * len(self.sorted_node_list) +
            # alpha multilayer excite
            [1e-9] * len(type(self.layer)) +
            # alpha shifted self excite
            [0.5] * len(self.self_excite_time_shifts))
        # Initialize the self-excitement param in the mutual excite list higher
        self.params[self.sorted_node_list.index(self.node) + 2] = 0.5

        # Nan out non-neighbors for graph regularization
        # (Will be treated as 0)
        if self.regularization == 1:
            for i, node in enumerate(self.sorted_node_list):
                if node != self.node and not self.intralayer_network.has_edge(node, self.node):
                    self.params[i+2] = np.nan
        elif self.regularization == 0:
            for i, node in enumerate(self.sorted_node_list):
                if node != self.node:
                    self.params[i+2] = np.nan
        elif self.regularization == -1:
            for i, node in enumerate(self.sorted_node_list):
                self.params[i+2] = np.nan
        elif self.regularization == np.inf:
            pass
        else:
            raise NotImplementedError

        if self.multilayer_excite:
            # Nan out the modeled layer's multilayer excite param,
            # which is redundant with self excitement.
            self.params[2+len(self.sorted_node_list)+list(type(self.layer)
                                                          ).index(self.layer)] = np.nan
        else:
            # Nan out all these disabled params.
            for i in range(2+len(self.sorted_node_list), 2+len(self.sorted_node_list)+len(type(self.layer))):
                self.params[i] = np.nan

    def _pack_param_constraints(self, params: NDArray) -> NDArray:
        # removing any nan params for regularization
        # also removes redundant layer nan param
        params = params[~np.isnan(params)]

        params[0] = np.log(params[0])  # positive
        params[1] = logit(params[1])  # probability
        params[2:] = logit(params[2:])  # 0 < alpha < 1 for stationarity

        if self.self_excite_time_shifts:
            # dummy param for remaining unused excitement up to constraint
            params = np.concatenate([params, [logit(0.5)]])

        return params

    def _unpack_param_constraints(self, params: NDArray) -> NDArray:
        params[0] = np.exp(params[0])
        params[1] = expit(params[1])
        params[2:] = expit(params[2:])

        if self.self_excite_time_shifts:
            # hold on to and remove dummy param
            dummy_param = params[-1]
            params = params[:-1]

        # restoring nan-ed out params
        params = utils.restore_nan_placeholder_params(
            params=params, like=self.params)

        if self.self_excite_time_shifts:
            normalization_factor = (
                # unshifted self-excitement
                params[self.sorted_node_list.index(self.node) + 2] +
                # shifted self-excitement
                sum(params[-len(self.self_excite_time_shifts):]) +
                # dummy param
                dummy_param
            )
            # normalize
            params[self.sorted_node_list.index(
                self.node) + 2] /= normalization_factor
            for i in range(len(self.self_excite_time_shifts)):
                params[-i-1] /= normalization_factor

        return params

    def fit(self,
            node_Yts: List[NDArray],
            layer_Yts: List[NDArray],
            sorted_node_list: List[str],
            intralayer_network: nx.Graph,
            enable_basinhopping: bool = True):
        """Fits the model to the data.

        Args:
            node_Yts: list of the event data for each node, same order as `self.sorted_node_list`.
            layer_Yts: list of the event data for each layer, same order as `Layer`.
            sorted_node_list: The graph's full vertex set as an alphabetized list.
            intralayer_network: The intralayer network structure.
            enable_basinhopping: Whether to enable basinhopping or just a single iteration of optimization.
        """
        if self.params is None:
            self.init_params(sorted_node_list, intralayer_network)

        start_time = time.time()
        optimization_result = basinhopping(
            func=self._nll,
            x0=self._pack_param_constraints(self.params),
            stepsize=2,
            minimizer_kwargs={
                'args': (node_Yts, layer_Yts),
                'method': 'L-BFGS-B',
                'options': {'maxiter': 1e6},
            },
            niter=100 if enable_basinhopping else 0,
            niter_success=20 if enable_basinhopping else None,
            # callback=lambda x, y, z: print(y),
        )
        end_time = time.time()
        print(
            f"Optimization took {np.round((end_time - start_time)/60, decimals=1)} minutes.")
        assert optimization_result.lowest_optimization_result.success, optimization_result.lowest_optimization_result.message
        self.params = self._unpack_param_constraints(
            optimization_result.lowest_optimization_result.x)
