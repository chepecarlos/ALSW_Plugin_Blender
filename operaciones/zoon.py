import bpy
import math

from .FuncionesArchivos import ObtenerValor, SalvarValor
from .extras import mostrarMensajeBox

from bpy.props import (
    BoolProperty,
    FloatProperty,
    EnumProperty,
    IntProperty,
)

class superzoon(bpy.types.Operator):
    bl_idname = "scene.superzoon"
    bl_label = "Super Zoon"
    bl_description = "Cambia el zoon en clip"
    bl_options = {"REGISTER", "UNDO"}

    macros: BoolProperty(
        name="macro",
        description="funcion con macro para zoon",
        default=False
    )

    incrementro: BoolProperty(
        name="Incrementro",
        description="incremento el zoon",
        default=False
    )

    zoon: FloatProperty(
        name="zoon",
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

    def execute(self, context):

        if len(bpy.context.selected_sequences) > 0:
            ClipActual = context.selected_sequences[0]

            if ClipActual.type != "MOVIE" and ClipActual.type != "IMAGE":
                return{'FINISHED'}

            ClipActual = context.selected_sequences[0]
            EsenaActual = context.scene.sequence_editor.active_strip.elements[0]
            AnchoCamva = context.scene.render.resolution_x
            AltoCamva = context.scene.render.resolution_y
            Alto = EsenaActual.orig_height
            Ancho = EsenaActual.orig_width
            # Codigo feo, pero funciona
            if ClipActual.use_proxy:
                # Buscar una forma no sucia
                MultiProxy = ObtenerValor("data/blender.json", "multi_proxy")
                if MultiProxy is None:
                    MultiProxy = 1
                Alto *= MultiProxy
                Ancho *= MultiProxy
            PosicionX = ClipActual.transform.offset_x
            PosicionY = ClipActual.transform.offset_y
            EscalaX = ClipActual.transform.scale_x
            EscalaY = ClipActual.transform.scale_y

            AnchoClip = Ancho * EscalaX
            AltoClip = Alto * EscalaY

            Relacion = math.sqrt(Alto * Alto + Ancho * Ancho)

            RelacionCanva = math.sqrt(AnchoCamva * AnchoCamva + AltoCamva * AltoCamva)

            RelacionRelativa = math.sqrt(AnchoClip * AnchoClip + AltoClip * AltoClip)

            MultiplicadorUnitario = RelacionCanva / Relacion

            if self.macros:
                if self.incrementro:
                    Aumentar = ObtenerValor("data/blender.json", "aumentar")
                    MultiplicadorRelativo = RelacionRelativa / Relacion
                    zoon = MultiplicadorRelativo + Aumentar
                else:
                    zoon = ObtenerValor("data/blender.json", "zoon")
            else:
                zoon = self.zoon

            ClipActual.transform.scale_x = MultiplicadorUnitario * zoon
            ClipActual.transform.scale_y = MultiplicadorUnitario * zoon
        else:
            mostrarMensajeBox("Selecione una pista", title="Error", icon="ERROR")

        return{'FINISHED'}