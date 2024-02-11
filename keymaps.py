from .keymap_ui import KeymapItemDef, KeymapStructure, KeymapLayout
from .operators import (
    GET_NODEGROUP_DEFAULTS,
    SET_NODEGROUP_DEFAULTS
)


keymap_info = {
    "keymap_name" : "Node Editor",
    "space_type" : "NODE_EDITOR",
}


keymap_structure = KeymapStructure([
    KeymapItemDef(GET_NODEGROUP_DEFAULTS.bl_idname, **keymap_info),
    KeymapItemDef(SET_NODEGROUP_DEFAULTS.bl_idname, **keymap_info),
    ]
)


keymap_layout = KeymapLayout(layout_structure=keymap_structure)


def register():
    keymap_structure.register()


def unregister():
    keymap_structure.unregister()
