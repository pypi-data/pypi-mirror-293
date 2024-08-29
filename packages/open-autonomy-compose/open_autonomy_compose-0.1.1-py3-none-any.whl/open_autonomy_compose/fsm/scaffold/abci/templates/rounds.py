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
# pylint: disable=import-error, too-few-public-methods, unused-import
"""This module contains the rounds definitions for __abci__."""

import typing as t
from enum import Enum

from packages.valory.skills.abstract_round_abci.base import (  # type: ignore[import] # noqa: F401
    AbciApp,
    AbciAppTransitionFunction,
    AppState,
    BaseSynchronizedData,
    CollectDifferentUntilThresholdRound,
    DegenerateRound,
)


class Event(Enum):
    """Event enumeration for the price estimation demo."""

    DONE = "done"
    ROUND_TIMEOUT = "round_timeout"
    NO_MAJORITY = "no_majority"


class SynchronizedData(BaseSynchronizedData):
    """Synchronised data."""


class ScaffoldedAbciApp(AbciApp[Event]):
    """AbciApp definition for __abci__"""

    initial_round_cls: AppState = object()
    initial_states: t.Set[AppState] = {}  # type: ignore[assignment]
    transition_function: AbciAppTransitionFunction = {}
    final_states: t.Set[AppState] = {}  # type: ignore[assignment]
    event_to_timeout: t.Dict[Event, float] = {
        Event.ROUND_TIMEOUT: 30.0,
    }
    db_pre_conditions: t.Dict[AppState, t.Set[str]] = {}
    db_post_conditions: t.Dict[AppState, t.Set[str]] = {}
