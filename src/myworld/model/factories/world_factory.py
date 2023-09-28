import i18n

from src.myworld.io.assets import Assets
from src.myworld.model.factories import node_factory
from src.myworld.model.world import World


def make_empty_world(project):
    default_world_material = _get_default_world_material(project.world_materials)
    return World(
        name=i18n.t("myworld.defaults.new_world_name"),
        material=default_world_material,
    )


def load_world_from_dict(world_dict, project):
    # TODO: validate world

    metadata = world_dict["metadata"]
    data = world_dict["data"]
    tag_data = data["tags"]
    world_data = data["world"]

    return World(
        name=metadata["world"]["name"],
        material=project.world_materials[world_data["material"]],
        nodes=[node_factory.load_node_from_tuple(tuple(node_data)) for node_data in world_data["nodes"]],
    )


def _get_default_world_material(world_materials):
    return world_materials[Assets.world_materials["default"]]
