import bpy
import os

from bpy.props import (
    BoolProperty,
    FloatProperty,
    EnumProperty,
    IntProperty,
)
from bpy.types import Volume

from .FuncionesArchivos import ObtenerValor, SalvarValor
from .extras import MostarMensajeBox


class superinsertar(bpy.types.Operator):
    bl_idname = "scene.superinsertar"
    bl_label = "Insertar Clip"
    bl_description = "Insertar imagen, video o audio en posicion de curso"
    bl_options = {"REGISTER", "UNDO"}

    desface: IntProperty(
        name="desface",
        description="desface de clip",
        default=0,
    )

    duracion: IntProperty(
        name="duracion",
        description="duracion de clip",
        default=60,
        min=0,
    )

    volumen: FloatProperty(name="volumen", description="volumen de Audio", default=1, min=0)

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

        if not os.path.isfile(ClipActual):
            MostarMensajeBox(f"Archivo no Existe {ClipActual}", title="Error", icon="ERROR")
            self.report({"INFO"}, f"Archivo no Existe {ClipActual}")
            return {"FINISHED"}

        Volumen = ObtenerValor("data/blender.json", "volumen")
        if Volumen is None:
            Volumen = self.volumen
        self.report({"INFO"}, f"Volumen: {Volumen}")

        Desface = ObtenerValor("data/blender.json", "desface")
        if Desface is None:
            Desface = self.desface
        self.report({"INFO"}, f"Desface: {Desface}")

        Duracion = ObtenerValor("data/blender.json", "duracion")
        if Duracion is None:
            Duracion = self.duracion
        self.report({"INFO"}, f"Duracion: {Duracion}")

        Tipo = ClipActual.split(".")[-1].lower()
        print(f"Tipo de Archivo {Tipo} de {ClipActual}")

        FrameActual = context.scene.frame_current

        if Tipo in ("jpg", "jpeg", "bmp", "png", "gif", "tga", "tiff"):

            # FolderActual = os.path.dirname(ClipActual)

            FolderActual = ClipActual.split("/")
            Archivo = FolderActual[-1]
            FolderActual = FolderActual[:-1]
            FolderActual = "/".join(FolderActual)
            FolderActual = FolderActual + "/"
            bpy.ops.sequencer.image_strip_add(
                directory=FolderActual,
                files=[{"name": Archivo, "name": Archivo}],
                frame_start=FrameActual + Desface,
                frame_end=FrameActual + Desface + Duracion,
                channel=1,
            )
            for Secuencia in context.selected_sequences:
                Secuencia.blend_type = "ALPHA_OVER"

        elif Tipo in ("avi", "mp4", "mpg", "mpeg", "mov", "mkv", "dv", "flv"):
            bpy.ops.sequencer.movie_strip_add(filepath=ClipActual, frame_start=FrameActual + Desface, channel=1)
        elif Tipo in ("acc", "ac3", "flac", "mp2", "mp3", "m4a", "pcm", "ogg"):
            bpy.ops.sequencer.sound_strip_add(filepath=ClipActual, frame_start=FrameActual + Desface, channel=1)
        else:
            MostarMensajeBox("Formato no reconocido habla con ChepeCarlos", title="Error", icon="ERROR")
            return {"FINISHED"}

        for Secuencia in context.selected_sequences:
            if Secuencia.type == "SOUND":
                Secuencia.show_waveform = True
                if Volumen is not None:
                    Secuencia.volume = Volumen

        SalvarValor("data/blender.json", "volumen", None)
        SalvarValor("data/blender.json", "ClipActual", None)
        return {"FINISHED"}
