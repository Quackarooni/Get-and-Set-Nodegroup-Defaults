import bpy
from .operators import (
    GET_NODEGROUP_DEFAULTS,
    SET_NODEGROUP_DEFAULTS
)

addon_keymaps = []
keymap_defs = (
    (GET_NODEGROUP_DEFAULTS.bl_idname, 'NONE', None),
    (SET_NODEGROUP_DEFAULTS.bl_idname, 'NONE', None),
)

def register():
    addon_keymaps.clear()
    key_config = bpy.context.window_manager.keyconfigs.addon

    if key_config:
        key_map = key_config.keymaps.new(
            name='Node Editor', space_type="NODE_EDITOR")
        for operator, key, props in keymap_defs:
            keymap_item = key_map.keymap_items.new(
                operator, key, value='PRESS')

            addon_keymaps.append((key_map, keymap_item))


def unregister():
    for key_map, key_entry in addon_keymaps:
        key_map.keymap_items.remove(key_entry)
    addon_keymaps.clear()
