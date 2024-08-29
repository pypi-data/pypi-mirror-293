# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright __year__ __author__
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""This package contains round behaviours of ScaffoldedAbciApp."""

from packages.valory.skills.abstract_round_abci.abci_app_chain import (  # type: ignore[import]
    AbciAppTransitionMapping,
    chain,
)


# TODO: transtions
abci_app_transition_mapping: AbciAppTransitionMapping = {}

ScaffoldedAbciApp = chain(
    tuple(),
    abci_app_transition_mapping,
)
