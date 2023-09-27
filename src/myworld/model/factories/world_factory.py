import i18n
from pygame import Color

from src.myworld.model.project import Project
from src.myworld.model.material import Material
from src.myworld.model.world import World
from src.myworld.io.assets import Assets


def make_empty_world(project):
    default_world_material = _get_default_world_material(project.world_materials)
    return World(
        name=i18n.t("myworld.defaults.new_world_name"),
        material=default_world_material,
    )


def _get_default_world_material(world_materials):
    return world_materials[Assets.world_materials["default"]]
