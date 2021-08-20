import bpy

from bpy.props import (
    BoolProperty,
    FloatProperty,
    EnumProperty,
    IntProperty,
)

from .FuncionesArchivos import ObtenerValor, SalvarValor
from .extras import MostarMensajeBox

class insertarsonido(bpy.types.Operator):
    bl_idname = "scene.insertarsonido"
    bl_label = "Insert sonido"
    bl_description = "Insertar sonido donde esta el cursor"
    bl_options = {"REGISTER", "UNDO"}

    macros: BoolProperty(
        name="macro",
        description="funcion con macro para zoon",
        default=False
    )

    # Verifica que este alguna secuencia selecionada
    @classmethod
    def poll(cls, context):
        return True
        # return context.selected_sequences

    def execute(self, context):
        if self.macros:
            FrameActual = context.scene.frame_current
            SonidoActual = ObtenerValor("data/blender.json", "sonido")
            Volumen = ObtenerValor("data/blender.json", "volumen")
            if SonidoActual is None:
                return{'FINISHED'}

            bpy.ops.sequencer.sound_strip_add(filepath=SonidoActual, frame_start=FrameActual, channel=1)

            context.selected_sequences[0].show_waveform = True
            if Volumen is not None:
                context.selected_sequences[0].volume = Volumen

            SalvarValor("data/blender.json", "sonido", None)
            SalvarValor("data/blender.json", "volumen", None)

        return{'FINISHED'}