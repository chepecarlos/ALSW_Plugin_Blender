import bpy

from bpy.props import (
    BoolProperty,
    FloatProperty,
    EnumProperty,
    IntProperty,
)

from .FuncionesArchivos import ObtenerValor, SalvarValor
from .extras import MostarMensajeBox

class superinsertar(bpy.types.Operator):
    bl_idname = "scene.superinsertar"
    bl_label = "Insertar Clip"
    bl_description = "Insertar imagen, video o audio en posicion de curso"
    bl_options = {"REGISTER", "UNDO"}

    macros: BoolProperty(name="macro", description="funcion con macro para zoon", default=False)

    @classmethod
    def poll(cls, context):
        return True
        # return context.selected_sequences

    def execute(self, context):

        if self.macros:
            ClipActual = ObtenerValor("data/blender.json", "clip")
        else:
            return {"FINISHED"}

        if ClipActual is None:
            MostarMensajeBox("Pista No asignada en: data/blender.json", title="Error", icon="ERROR")
            return {"FINISHED"}

        Volumen = ObtenerValor("data/blender.json", "volumen")
        Tipo = ClipActual.split(".")[-1].lower()
        print(f"Tipo de Archivo {Tipo} de {ClipActual}")

        FrameActual = context.scene.frame_current

        if Tipo in ("jpg", "jpeg", "bmp", "png", "gif", "tga", "tiff"):
            FolderActual = ClipActual.split("/")
            Archivo = FolderActual[-1]
            FolderActual = FolderActual[:-1]
            FolderActual = "/".join(FolderActual)
            bpy.ops.sequencer.image_strip_add(
                directory=FolderActual,
                files=[{"name": Archivo, "name": Archivo}],
                frame_start=FrameActual,
                frame_end=FrameActual + 60,
                channel=1,
            )
        elif Tipo in ("avi", "mp4", "mpg", "mpeg", "mov", "mkv", "dv", "flv"):
            bpy.ops.sequencer.movie_strip_add(filepath=ClipActual, frame_start=FrameActual, channel=1)
            for Secuencia in context.selected_sequences:
                if Secuencia.type == 'SOUND':
                    Secuencia.show_waveform = True
                    if Volumen is not None:
                        Secuencia.volume = Volumen

        elif Tipo in ("acc", "ac3", "flac", "mp2", "mp3", "m4a", "pcm", "ogg"):
            bpy.ops.sequencer.sound_strip_add(filepath=ClipActual, frame_start=FrameActual, channel=1)
            context.selected_sequences[0].show_waveform = True
            if Volumen is not None:
                context.selected_sequences[0].volume = Volumen
        else:
            MostarMensajeBox("Formato no reconocido habla con ChepeCarlos", title="Error", icon="ERROR")
        
        
        SalvarValor("data/blender.json", "volumen", None)
        SalvarValor("data/blender.json", "ClipActual", None)
        return {"FINISHED"}
