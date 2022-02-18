import os
from math import pi

import bpy
from bpy.props import BoolProperty, EnumProperty, FloatProperty, IntProperty
from bpy.types import Volume

from .extras import MostarMensajeBox
from .FuncionesArchivos import ObtenerValor, SalvarValor


class superinsertar(bpy.types.Operator):
    bl_idname = "scene.superinsertar"
    bl_label = "Insertar Clip"
    bl_description = "Insertar imagen, video o audio en posición de curso"
    bl_options = {"REGISTER", "UNDO"}

    desface: IntProperty(
        name="desface",
        description="desface de clip",
        default=0,
    )

    duracion: IntProperty(
        name="duracion",
        description="duracion del clip",
        default=60,
        min=0,
    )

    posicion_x: IntProperty(name="posición x", description="Posición x del clip", default=0)
    posicion_y: IntProperty(name="posición y", description="Posición y del clip", default=0)
    angulo: FloatProperty(name="angulo", description="Angulo del Cip", default=0, max=360)

    origen_x: FloatProperty(name="oringe x", description="Origen x del Cip", default=0.5, min=0, max=1)
    origen_y: FloatProperty(name="oringe y", description="Origen y del Cip", default=0.5, min=0, max=1)

    opacidad: FloatProperty(name="opacidad", description="Opacidad del clip", default=1, min=0, max=1)

    volumen: FloatProperty(name="volumen", description="Volumen de Audio", default=1, min=0)

    macros: BoolProperty(name="macro", description="Funcion con macro para zoon", default=False)

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

        data = ObtenerValor("data/blender.json", "volumen")
        if data is None:
            self.volumen = data

        data = ObtenerValor("data/blender.json", "desface")
        if data is not None:
            self.desface = data

        data = ObtenerValor("data/blender.json", "duracion")
        if data is not None:
            self.duracion = data

        data = ObtenerValor("data/blender.json", "posicion_x")
        if data is not None:
            self.posicion_x = data

        data = ObtenerValor("data/blender.json", "opacidad")
        if data is not None:
            self.opacidad = data

        data = ObtenerValor("data/blender.json", "posicion_y")
        if data is not None:
            self.posicion_y = data

        data = ObtenerValor("data/blender.json", "angulo")
        if data is not None:
            self.angulo = data

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
            elif Secuencia.type == "IMAGE" or Secuencia.type == "MOVIE":
                Secuencia.blend_type = "ALPHA_OVER"
                Secuencia.transform.rotation = self.angulo * (pi / 180)
                Secuencia.transform.offset_x = self.posicion_x
                Secuencia.transform.offset_y = self.posicion_y
                Secuencia.blend_alpha = self.opacidad
                Secuencia.transform.origin[0] = self.origen_x
                Secuencia.transform.origin[1] = self.origen_y

        atributos = {"posicion_x", "posicion_y", "opacidad", "volumen", "desface", "origen_x", "origen_y"}

        for atributo in atributos:
            SalvarValor("data/blender.json", atributo, None)

        return {"FINISHED"}
