from typing import Optional

from simaple.core.base import Stat
from simaple.simulate.base import Entity
from simaple.simulate.component.base import ReducerState, reducer_method, view_method
from simaple.simulate.component.entity import Cooldown, Periodic, Stack
from simaple.simulate.component.skill import SkillComponent
from simaple.simulate.component.trait.impl import (
    CooldownValidityTrait,
    InvalidatableCooldownTrait,
    PeriodicWithSimpleDamageTrait,
    UseSimpleAttackTrait,
)
from simaple.simulate.component.view import Running
from simaple.simulate.global_property import Dynamics


class DivineMark(Entity):
    advantage: Optional[Stat] = None

    def mark(self, advantage: Stat):
        self.advantage = advantage

    def consume_mark(self) -> Stat:
        self.advantage, advantage = None, self.advantage
        if advantage is None:
            advantage = Stat()

        return advantage


class DivineAttackSkillState(ReducerState):
    divine_mark: DivineMark
    cooldown: Cooldown
    dynamics: Dynamics


class DivineAttackSkillComponent(
    SkillComponent, CooldownValidityTrait, UseSimpleAttackTrait
):
    binds: dict[str, str] = {
        "divine_mark": ".바하뮤트.divine_mark",
    }
    name: str
    damage: float
    hit: float
    cooldown_duration: float
    delay: float
    synergy: Optional[Stat] = None

    def get_default_state(self):
        return {
            "cooldown": Cooldown(time_left=0),
        }

    @reducer_method
    def use(self, _: None, state: DivineAttackSkillState):
        state = state.deepcopy()

        if not state.cooldown.available:
            return state, self.event_provider.rejected()

        state.cooldown.set_time_left(
            state.dynamics.stat.calculate_cooldown(self.cooldown_duration)
        )

        modifier = state.divine_mark.consume_mark()

        return state, [
            self.event_provider.dealt(self.damage, self.hit, modifier=modifier),
            self.event_provider.delayed(self.delay),
        ]

    @reducer_method
    def elapse(self, time: float, state: DivineAttackSkillState):
        return self.elapse_simple_attack(time, state)

    @view_method
    def validity(self, state: DivineAttackSkillState):
        return self.validity_in_cooldown_trait(state)

    @view_method
    def buff(self, _: DivineAttackSkillState):
        return self.synergy

    def _get_simple_damage_hit(self) -> tuple[float, float]:
        return self.damage, self.hit


class DivineMinionState(ReducerState):
    divine_mark: DivineMark
    cooldown: Cooldown
    periodic: Periodic
    dynamics: Dynamics


class DivineMinion(
    SkillComponent, PeriodicWithSimpleDamageTrait, InvalidatableCooldownTrait
):
    name: str
    damage: float
    hit: float
    cooldown_duration: float
    delay: float

    periodic_interval: float
    periodic_damage: float
    periodic_hit: float
    lasting_duration: float

    mark_advantage: Stat
    stat: Optional[Stat] = None

    def get_default_state(self):
        if self.name == "바하뮤트":
            return {
                "divine_mark": DivineMark(),
                "cooldown": Cooldown(time_left=0),
                "periodic": Periodic(interval=self.periodic_interval, time_left=0),
            }

        return {
            "cooldown": Cooldown(time_left=0),
            "periodic": Periodic(interval=self.periodic_interval, time_left=0),
        }

    @reducer_method
    def elapse(self, time: float, state: DivineMinionState):
        state = state.deepcopy()

        state.cooldown.elapse(time)
        dealing_events = []

        for _ in state.periodic.resolving(time):
            state.divine_mark.mark(self.mark_advantage)
            dealing_events.append(
                self.event_provider.dealt(
                    self.periodic_damage,
                    self.periodic_hit,
                )
            )

        return state, [self.event_provider.elapsed(time)] + dealing_events

    @view_method
    def buff(self, state: DivineMinionState):
        if state.periodic.enabled():
            return self.stat

        return None

    @reducer_method
    def use(self, _: None, state: DivineMinionState):
        return self.use_periodic_damage_trait(state)

    @view_method
    def validity(self, state: DivineMinionState):
        return self.validity_in_invalidatable_cooldown_trait(state)

    @view_method
    def running(self, state: DivineMinionState) -> Running:
        return Running(
            id=self.id,
            name=self.name,
            time_left=state.periodic.time_left,
            lasting_duration=self._get_lasting_duration(state),
        )

    def _get_lasting_duration(self, state: DivineMinionState) -> float:
        return self.lasting_duration

    def _get_simple_damage_hit(self) -> tuple[float, float]:
        return self.damage, self.hit

    def _get_periodic_damage_hit(self, state: DivineMinionState) -> tuple[float, float]:
        return self.periodic_damage, self.periodic_hit


class HexaAngelRayState(ReducerState):
    divine_mark: DivineMark
    cooldown: Cooldown
    dynamics: Dynamics
    punishing_stack: Stack


class HexaAngelRayComponent(
    SkillComponent, CooldownValidityTrait, UseSimpleAttackTrait
):
    binds: dict[str, str] = {
        "divine_mark": ".바하뮤트.divine_mark",
    }
    name: str
    damage: float
    hit: float
    delay: float

    punishing_damage: float
    punishing_hit: float
    stack_resolve_amount: int

    synergy: Stat

    def get_default_state(self):
        return {
            "cooldown": Cooldown(time_left=0),
            "punishing_stack": Stack(
                maximum_stack=self.stack_resolve_amount * 2 - 1
            ),  # one-buffer
        }

    @reducer_method
    def use(self, _: None, state: HexaAngelRayState):
        state = state.deepcopy()

        if not state.cooldown.available:
            return state, self.event_provider.rejected()

        state.cooldown.set_time_left(
            state.dynamics.stat.calculate_cooldown(self.cooldown_duration)
        )
        state, stack_events = self._stack(state)

        modifier = state.divine_mark.consume_mark()

        return (
            state,
            [
                self.event_provider.dealt(self.damage, self.hit, modifier=modifier),
                self.event_provider.delayed(self.delay),
            ]
            + stack_events,
        )

    @reducer_method
    def stack(self, _: None, state: HexaAngelRayState):
        return self._stack(state)

    def _stack(self, state: HexaAngelRayState):
        """
        Add 1 stack for Holy Punishing.

        This method can be called internally, or
        can be called by Divine Punishmenet.
        """
        state = state.deepcopy()
        state.punishing_stack.increase(1)
        if state.punishing_stack.get_stack() >= self.stack_resolve_amount:
            state.punishing_stack.decrease(self.stack_resolve_amount)

            return state, [
                self.event_provider.dealt(self.punishing_damage, self.punishing_hit)
            ]

        return state, []

    @reducer_method
    def elapse(self, time: float, state: HexaAngelRayState):
        return self.elapse_simple_attack(time, state)

    @view_method
    def validity(self, state: HexaAngelRayState):
        return self.validity_in_cooldown_trait(state)

    @view_method
    def buff(self, _: HexaAngelRayState):
        return self.synergy

    def _get_simple_damage_hit(self) -> tuple[float, float]:
        return self.damage, self.hit
