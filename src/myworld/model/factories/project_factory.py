import i18n
from pygame import Color

from src.myworld.model.project import Project
from src.myworld.model.material import Material
from src.myworld.model.world import World
from src.myworld.resources.assets import Assets


def make_empty_project():
    world_materials = _get_default_world_materials()
    default_world_material = _get_default_world_material(world_materials)
    return Project(
        world_materials=world_materials,
        worlds=[World(
            name=i18n.t("myworld.defaults.new_world_name"),
            material=default_world_material,
        )]
    )

def _get_default_world_materials():
    return {
        k: Material(
            color=Color(v["color"])
        )
        for k, v in Assets.world_materials["materials"].items()
    }


def _get_default_world_material(world_materials):
    return world_materials[Assets.world_materials["default"]]
