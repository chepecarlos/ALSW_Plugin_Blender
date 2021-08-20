import bpy

from bpy.props import (
    BoolProperty,
    FloatProperty,
    EnumProperty,
    IntProperty,
)

from .FuncionesArchivos import ObtenerValor, SalvarValor
from .extras import MostarMensajeBox


class insertaraudio(bpy.types.Operator):
    bl_idname = "scene.insertaraudio"
    bl_label = "Insert Video"
    bl_description = "Insertar pista de audio sobre otra clip"
    bl_options = {"REGISTER", "UNDO"}

    macros: BoolProperty(
        name="macro",
        description="funcion con macro para zoon",
        default=False
    )

    # Verifica que este alguna secuencia selecionada
    @classmethod
    def poll(cls, context):
        return context.selected_sequences

    def execute(self, context):

        if self.macros:
            VideoActual = ObtenerValor("data/blender.json", "clip")
        else:
            return{'FINISHED'}

        # context.area.type = 'SEQUENCE_EDITOR'
        # FrameActual = bpy.context.scene.frame_current
        if VideoActual is None:
            MostarMensajeBox("Pista No asignada en: data/blender.json",
                             title="Error", icon="ERROR")
            return{'FINISHED'}
            
        # TODO: Buscar inicio y fin de selecion de clips en ves de solo el primero
        if len(context.selected_sequences) > 0:
            Inicio = context.selected_sequences[0].frame_final_start
            Final = context.selected_sequences[0].frame_final_end
            Canal = context.selected_sequences[0].channel + 1

            bpy.ops.sequencer.sound_strip_add(
                filepath=VideoActual, frame_start=Inicio, channel=Canal)

            context.selected_sequences[0].show_waveform = True
            context.selected_sequences[0].volume = 0.3

            bpy.ops.sequencer.split(
                frame=Final, channel=Canal, type='SOFT', side='RIGHT')

            bpy.ops.sequencer.delete()

            # bpy.context.selected_sequences[0].use_proxy = True
        else:
            MostarMensajeBox("Selecione una pista",
                             title="Error", icon="ERROR")
        SalvarValor("data/blender.json", "clip", None)
        return{'FINISHED'}
