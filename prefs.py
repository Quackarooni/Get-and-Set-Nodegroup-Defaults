import bpy
from bpy.props import BoolProperty, EnumProperty
from .keymaps import keymap_layout

class GetSetDefaultsPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    show_keymaps: BoolProperty(
        name="Show Keymaps",
        default=False,
        description="When enabled, displays keymap list",
    )

    apply_to: EnumProperty(
        name="Apply to",
        items=(
            ("UNLINKED", "Only Visible & Unlinked", "Apply operators to all inputs that are not hidden and linked to anything"),
            ("VISIBLE", "Only Visible", "Apply operators to all inputs that are not hidden"),
            ("ALL", "All Inputs", "Apply operators to all inputs of the nodegroup"),
        ),
        default='ALL',
        description="Specifies which sockets the operators get applied to."
    )

    def draw(self, context):
        layout = self.layout

        layout.prop(self, "apply_to")
        keymap_layout.draw_keyboard_shorcuts(self, layout, context)


keymap_layout.register_properties(preferences=GetSetDefaultsPreferences)


classes = (
    GetSetDefaultsPreferences,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
