import bpy

from bpy.props import (
    BoolProperty,
    FloatProperty,
    EnumProperty,
    IntProperty,
)

from .FuncionesArchivos import ObtenerValor, SalvarValor
from .extras import MostarMensajeBox


class moverclip(bpy.types.Operator):
    bl_idname = "scene.moverclip"
    bl_label = "mover clip"
    bl_description = "mover clip en una direcion"
    bl_options = {"REGISTER", "UNDO"}

    macros: BoolProperty(
        name="macro",
        description="funcion con macro para alinacion",
        default=False
    )

    movimiento_horizontal: FloatProperty(
        name="movimiento_horizontal",
        description="zoon para clip",
        default=1,
        min=-10, max=10
    )

    movimiento_vertical: FloatProperty(
        name="movimiento_vertical",
        description="zoon para clip",
        default=1,
        min=-10, max=10
    )

    # Verifica que este alguna secuencia selecionada
    @classmethod
    def poll(cls, context):
        # Todo: Solo activar con clip de video
        if len(bpy.context.selected_sequences) > 0:
            ClipActual = context.selected_sequences[0]
            if ClipActual.type != "MOVIE" and ClipActual.type != "IMAGE":
                return False
            return context.selected_sequences
        return False

    def execute(self, context):

        if len(bpy.context.selected_sequences) > 0:
            ClipActual = context.selected_sequences[0]
            EsenaActual = context.scene.sequence_editor.active_strip.elements[0]

            movimiento_horizontal = self.movimiento_horizontal
            movimiento_vertical = self.movimiento_vertical
            if self.macros:
                movimiento_horizontal = ObtenerValor(
                    "data/blender.json", "movimiento_horizontal")
                movimiento_vertical = ObtenerValor(
                    "data/blender.json", "movimiento_vertical")
                if movimiento_horizontal is None:
                    movimiento_horizontal = 0
                if movimiento_vertical is None:
                    movimiento_vertical = 0

            Ancho = EsenaActual.orig_width
            Alto = EsenaActual.orig_height

            print(Ancho, Alto)
            ClipActual.transform.offset_x += movimiento_vertical * Ancho
            ClipActual.transform.offset_y += movimiento_horizontal * Alto

            SalvarValor("data/blender.json", "movimiento_horizontal", None)
            SalvarValor("data/blender.json", "movimiento_vertical", None)

        return{'FINISHED'}
