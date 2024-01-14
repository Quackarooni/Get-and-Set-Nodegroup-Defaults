import bpy
from bpy.props import BoolProperty, EnumProperty
from . import keymap_ui
from .operators import fetch_user_preferences

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
        keymap_ui.draw_keyboard_shorcuts(self, layout, context)


classes = (
    GetSetDefaultsPreferences,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    prefs = fetch_user_preferences()
    prefs.property_unset("show_keymaps")

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
