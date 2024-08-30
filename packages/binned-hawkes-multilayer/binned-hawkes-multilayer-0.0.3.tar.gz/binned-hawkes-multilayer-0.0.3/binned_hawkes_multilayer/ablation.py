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

Description: Models for the ablation study on the proposed model.
"""


from enum import Enum

from binned_hawkes_multilayer.proposed import ProposedModel


class AblationModel1(ProposedModel):
    def __init__(self, node: str, layer: Enum):
        super().__init__(node, layer,
                         regularization=1,
                         self_excite_time_shifts=[24, 168],
                         multilayer_excite=False)


class AblationModel2(ProposedModel):
    def __init__(self, node: str, layer: Enum):
        super().__init__(node, layer,
                         regularization=1,
                         self_excite_time_shifts=[],
                         multilayer_excite=True)


class AblationModel3(ProposedModel):
    def __init__(self, node: str, layer: Enum):
        super().__init__(node, layer,
                         regularization=0,
                         self_excite_time_shifts=[24, 168],
                         multilayer_excite=True)


class AblationModel4(ProposedModel):
    """regularized mutually exciting model"""

    def __init__(self, node: str, layer: Enum):
        super().__init__(node, layer,
                         regularization=1,
                         self_excite_time_shifts=[],
                         multilayer_excite=False)


class AblationModel5(ProposedModel):
    """shifted self exciting model"""

    def __init__(self, node: str, layer: Enum):
        super().__init__(node, layer,
                         regularization=0,
                         self_excite_time_shifts=[24, 168],
                         multilayer_excite=False)


class AblationModel6(ProposedModel):
    """multilayer contextual model"""

    def __init__(self, node: str, layer: Enum):
        super().__init__(node, layer,
                         regularization=0,
                         self_excite_time_shifts=[],
                         multilayer_excite=True)


class AblationModel7(ProposedModel):
    """self exciting model"""

    def __init__(self, node: str, layer: Enum):
        super().__init__(node, layer,
                         regularization=0,
                         self_excite_time_shifts=[],
                         multilayer_excite=False)


class AblationModel8(ProposedModel):
    """no excitation / homogenous model"""

    def __init__(self, node: str, layer: Enum):
        super().__init__(node, layer,
                         regularization=-1,
                         self_excite_time_shifts=[],
                         multilayer_excite=False)


ABLATION_MODELS = (
    ProposedModel,
    AblationModel1,
    AblationModel2,
    AblationModel3,
    AblationModel4,
    AblationModel5,
    AblationModel6,
    AblationModel7,
    AblationModel8,
)

COLORS = (
    'gray',
    '#d9f0d3',  # green
    '#decbe4',  # purple
    '#fed9a6',  # orange
    '#c6e2ff',  # blue
    '#ffffcc',  # yellow
    '#fbb4ae',  # red
    'white',
    'white',
)
