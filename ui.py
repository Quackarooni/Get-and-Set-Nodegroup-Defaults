import bpy
from bpy.types import Panel
from .operators import fetch_user_preferences


class NODE_PT_SETGET_DEFAULTS_PANEL(Panel):
    bl_label = "Nodegroup Defaults"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = "UI"
    bl_category = "Group"
    bl_order = 0

    @classmethod
    def poll(cls, context):
        space = context.space_data
        is_node_editor = (space.type == 'NODE_EDITOR')
        is_exists = (space.node_tree is not None)
        return all((is_node_editor, is_exists))

    def draw(self, context):
        layout = self.layout
        prefs = fetch_user_preferences()

        col = layout.column()
        col.label(text="Apply to:")
        col.prop(prefs, "apply_to", text="")
        col.separator()
        col.operator("node.get_nodegroup_defaults")
        col.operator("node.set_nodegroup_defaults")


classes = (
    NODE_PT_SETGET_DEFAULTS_PANEL,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
