from pygame import Color

from src.myworld.io.files import Files
from src.myworld.model.factories import world_factory
from src.myworld.model.material import Material
from src.myworld.model.project import Project
from src.myworld.io.assets import Assets


def make_empty_project():
    world_materials = _get_default_world_materials()
    project = Project(world_materials=world_materials, worlds=[])
    project.worlds.append(world_factory.make_empty_world(project))
    return project


def load_project_from_dict(project_dict, world_dicts=None):
    world_materials = _get_default_world_materials()
    project = Project(world_materials=world_materials, worlds=[])
    project.worlds = [world_factory.load_world_from_dict(world_dict, project) for world_dict in world_dicts]
    return project


def load_project_from_dir(
        project_dir_path,
        on_unexpected_file_found=None,
):
    files = Files.load_file_structure(
        dir_path=project_dir_path,
        schema={
            "project": [".yml", ".yaml", ".json"],
            "worlds": {
                "*": [".yml", ".yaml", ".json"],
            }
        },
        on_unexpected_file_found=on_unexpected_file_found
    )
    return load_project_from_dict(
        project_dict=files["project"],
        world_dicts=files["worlds"].values()
    )


def _get_default_world_materials():
    return {
        k: Material(
            color=Color(v["color"])
        )
        for k, v in Assets.world_materials["materials"].items()
    }
