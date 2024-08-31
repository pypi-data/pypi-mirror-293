from abc import abstractmethod

from pydantic import BaseModel

from simaple.core import Stat
from simaple.gear.blueprint.gear_blueprint import PracticalGearBlueprint
from simaple.gear.gearset import Gearset
from simaple.gear.potential import PotentialTier
from simaple.gear.setitem import SetItemRepository
from simaple.gear.slot_name import SlotName
from simaple.gear.symbol_gear import ArcaneSymbolTemplate, AuthenticSymbolTemplate
from simaple.spec.loadable import (  # pylint:disable=unused-import
    TaggedNamespacedABCMeta,
)


class GearsetBlueprint(BaseModel, metaclass=TaggedNamespacedABCMeta(kind="blueprint")):
    @abstractmethod
    def build(self, set_item_repository: SetItemRepository) -> Gearset: ...


# TODO: weapon potential optimizer (stand-alone)
class UserGearsetBlueprint(GearsetBlueprint):
    arcane_symbols: list[ArcaneSymbolTemplate] = []
    authentic_symbols: list[AuthenticSymbolTemplate] = []
    pet_equip: Stat
    pet_set: Stat
    cash: Stat
    weapon_potential_tiers: tuple[
        list[PotentialTier],
        list[PotentialTier],
        list[PotentialTier],
    ]
    title: Stat

    gears: dict[SlotName, PracticalGearBlueprint]

    def build(self, set_item_repository: SetItemRepository) -> Gearset:
        gearset = Gearset()

        for slot_name, blueprint in self.gears.items():
            gearset.equip(blueprint.build(), slot_name)

        gearset.set_title_stat(self.title)
        gearset.annotate_weapon_potential_tiers(self.weapon_potential_tiers)
        gearset.set_symbols(
            [
                symbol_template.get_symbol()
                for symbol_template in self.arcane_symbols + self.authentic_symbols
            ]
        )

        gearset.set_pet_equip_stat(self.pet_equip)
        gearset.set_pet_set_option(self.pet_set)
        gearset.set_cash_item_stat(self.cash)

        gearset.set_set_items(set_item_repository.get_all(gearset.get_gears()))

        return gearset
