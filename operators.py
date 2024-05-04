import bpy
from bpy.types import Operator


def fetch_user_preferences(attr_id=None):
    prefs = bpy.context.preferences.addons[__package__].preferences

    if attr_id is None:
        return prefs
    else:
        return getattr(prefs, attr_id)


def has_nodegroup(context):
    for node in context.selected_nodes:
        if node.type == 'GROUP':
            return True
        
    return False

def get_nodegroups(context):
    for node in context.selected_nodes:
        if node.type == 'GROUP':
            yield node


if bpy.app.version >= (4, 0, 0): 
    def get_inputs(tree):
        return (x for x in tree.interface.items_tree if (x.item_type == 'SOCKET' and x.in_out == 'INPUT'))
else:
    def get_inputs(tree):
        return tree.inputs


class GET_NODEGROUP_DEFAULTS(Operator):
    bl_label = "Get Defaults"
    bl_idname = "node.get_nodegroup_defaults"
    bl_description = "Retrieve a node's default values and sets it to be its current values"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    @classmethod
    def poll(cls, context):
        try:
            space = context.space_data
            is_node_editor = (space.type == 'NODE_EDITOR')
            is_exists = (space.node_tree is not None)
            return all((has_nodegroup(context), is_node_editor, is_exists))
            
        except AttributeError:
            return False

    def execute(self, context):
        update_count = 0
        total_count = 0

        apply_mode = fetch_user_preferences(attr_id="apply_to")

        for node in get_nodegroups(context):
            for inp, default in zip(node.inputs, get_inputs(node.node_tree)):

                if inp.type in ('SHADER', 'GEOMETRY'):
                    continue

                total_count += 1
                if (apply_mode == "UNLINKED") and (inp.is_linked or inp.hide or not inp.enabled):
                    continue
                elif (apply_mode == "VISIBLE") and (inp.hide or not inp.enabled):
                    continue

                inp.default_value = default.default_value
                update_count += 1

        self.report({'INFO'}, f"Succesfully updated {update_count} out of {total_count} current values.")
        return {'FINISHED'}


class SET_NODEGROUP_DEFAULTS(Operator):
    bl_label = "Set Defaults"
    bl_idname = "node.set_nodegroup_defaults"
    bl_description = "Retrieve a node's current values and sets it to be its default values"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    @classmethod
    def poll(cls, context):
        try:
            space = context.space_data
            is_node_editor = (space.type == 'NODE_EDITOR')
            is_exists = (space.node_tree is not None)

            are_groups_unique = len(list(get_nodegroups(context))) == len(set(node.node_tree for node in get_nodegroups(context)))
            return all((has_nodegroup(context), is_node_editor, is_exists, are_groups_unique))
        
        except AttributeError:
            return False

    def execute(self, context):
        update_count = 0
        total_count = 0
        apply_mode = fetch_user_preferences(attr_id="apply_to")

        for node in get_nodegroups(context):
            for inp, default in zip(node.inputs, get_inputs(node.node_tree)):
                if inp.type in ('SHADER', 'GEOMETRY'):
                    continue
                
                total_count += 1
                if (apply_mode == "UNLINKED") and (inp.is_linked or inp.hide or not inp.enabled):
                    continue
                elif (apply_mode == "VISIBLE") and (inp.hide or not inp.enabled):
                    continue

                default.default_value = inp.default_value
                update_count += 1

        self.report({'INFO'}, f"Succesfully updated {update_count} out of {total_count} default values.")
        return {'FINISHED'}


classes = (
    GET_NODEGROUP_DEFAULTS,
    SET_NODEGROUP_DEFAULTS,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
