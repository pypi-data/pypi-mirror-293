# pylint: disable=too-few-public-methods
"""FSM types."""

import typing as t
from enum import Enum


class EventsType(Enum):
    """Event type."""

    SENTINAL = "sentinal"
    DONE = "done"


class StatePosition(Enum):
    """State position."""

    START = "start"
    INITIAL = "initial"
    INTERMEDIATE = "intermediate"
    FINAL = "final"


class BaseRound(Enum):
    """Base round type enum"""

    DegenerateRound = "DegenerateRound"
    CollectionRound = "CollectionRound"
    CollectDifferentUntilAllRound = "CollectDifferentUntilAllRound"
    CollectSameUntilAllRound = "CollectSameUntilAllRound"
    CollectSameUntilThresholdRound = "CollectSameUntilThresholdRound"
    OnlyKeeperSendsRound = "OnlyKeeperSendsRound"
    VotingRound = "VotingRound"
    CollectDifferentUntilThresholdRound = "CollectDifferentUntilThresholdRound"
    CollectNonEmptyUntilThresholdRound = "CollectNonEmptyUntilThresholdRound"
    PendingOffencesRound = "PendingOffencesRound"


class StateType:
    """State type."""


class PayloadType:
    """Payload type."""


class BehaviourType:
    """Behaviour type."""


class RoundBehaviourType:
    """Round behaviour type."""


class AbciAppType:
    """AbciApp abstraction"""

    initial_round_cls: StateType
    initial_states: t.Set[StateType] = set()
    transition_function: "TransitionFunction"
    final_states: t.Set[StateType] = set()
    event_to_timeout: t.Dict[StateType, float] = {}
    cross_period_persisted_keys: t.FrozenSet[str] = frozenset()
    background_round_cls: t.Optional[StateType] = None
    termination_transition_function: t.Optional["TransitionFunction"] = None
    termination_event: t.Optional[StateType] = None
    default_db_preconditions: t.Set[str] = set()
    db_pre_conditions: t.Dict[StateType, t.Set[str]] = {}
    db_post_conditions: t.Dict[StateType, t.Set[str]] = {}


TransitionFunction = t.OrderedDict[StateType, t.OrderedDict[EventsType, StateType]]
