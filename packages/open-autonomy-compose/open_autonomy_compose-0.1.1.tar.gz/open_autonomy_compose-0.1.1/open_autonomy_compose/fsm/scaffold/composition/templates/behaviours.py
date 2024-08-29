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

"""This package contains behaviour implementations."""

import typing as t

from packages.__author__.skills.__abci__.composition import (
    ScaffoldedAbciApp,  # type: ignore[import]
)
from packages.valory.skills.abstract_round_abci.behaviours import (  # type: ignore[import]
    AbstractRoundBehaviour,
    BaseBehaviour,
)


class ScaffoldedConsensusBehaviour(AbstractRoundBehaviour):
    """Class to define the behaviours this AbciApp has."""

    initial_behaviour_cls = object
    abci_app_cls = ScaffoldedAbciApp
    behaviours: t.Set[t.Type[BaseBehaviour]] = set()
