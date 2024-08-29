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
# mypy: disable-error-code="import"

"""This module contains the shared state for the abci skill of ScaffoldedAbciApp."""

from packages.__author__.skills.__abci__.composition import (
    ScaffoldedAbciApp,  # type: ignore[import]
)
from packages.valory.skills.abstract_round_abci.models import (  # type: ignore[import]
    ApiSpecs,
    BaseParams,
)
from packages.valory.skills.abstract_round_abci.models import (
    BenchmarkTool as BaseBenchmarkTool,  # type: ignore[import]
)
from packages.valory.skills.abstract_round_abci.models import (
    Requests as BaseRequests,  # type: ignore[import]
)
from packages.valory.skills.abstract_round_abci.models import (
    SharedState as BaseSharedState,  # type: ignore[import]
)


Requests = BaseRequests
BenchmarkTool = BaseBenchmarkTool


class RandomnessApi(ApiSpecs):
    """A model that wraps ApiSpecs for randomness api specifications."""


class SharedState(BaseSharedState):
    """Keep the current shared state of the skill."""

    abci_app_cls = ScaffoldedAbciApp


class Params(BaseParams):
    """A model to represent params for multiple abci apps."""
