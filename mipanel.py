import bpy

class mipanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window."""
    bl_idname = "my.mipanel"
    bl_label = "Panel ALSW"
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'

    def draw(self, context):
        """Dibujar el panel."""
        layout = self.layout

        row = layout.row()
        row.label(text="Musica sobre clip", icon="SOUND")
        row = layout.row()
        ops = row.operator("scene.insertaraudio", text="MrTee")