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
# pylint: disable=import-error, too-few-public-methods, unnecessary-pass

"""This package contains behaviour implementations."""

import typing as t
from abc import ABC

from packages.__author__.skills.__abci__.rounds import (
    ScaffoldedAbciApp,  # type: ignore[import]
)
from packages.valory.skills.abstract_round_abci.behaviours import (
    AbstractRoundBehaviour,  # type: ignore[import]
)
from packages.valory.skills.abstract_round_abci.behaviours import (
    BaseBehaviour as AbstractBaseBehaviour,  # type: ignore[import]
)


class BaseBehaviour(AbstractBaseBehaviour, ABC):
    """Base behaviour for the FSM App."""


class InitialBehaviour(BaseBehaviour):
    """This behaviour manages the initial stage."""

    pass


class ScaffoldedRoundBehaviour(AbstractRoundBehaviour):
    """This behaviour manages the consensus stages."""

    initial_behaviour_cls = object()
    abci_app_cls = ScaffoldedAbciApp
    behaviours: t.Set[t.Type[BaseBehaviour]] = {
        InitialBehaviour,  # type: ignore
    }
