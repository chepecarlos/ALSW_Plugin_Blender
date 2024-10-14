import os
from math import pi

import bpy

from .extras import mostrarMensajeBox
from .FuncionesArchivos import ObtenerValor, SalvarValor, ObtenerArchivo
from .funcionesExtras import asignarDinámica


class superInsertar(bpy.types.Operator):
    bl_idname = "scene.superinsertar"
    bl_label = "Insertar Clip"
    bl_description = "Insertar imagen, video o audio en posición de curso"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        render = context.scene.render
        framerate = render.fps / render.fps_base

        self.report({"INFO"}, f"Insertando clips")

        dataInsertar = ObtenerArchivo("data/insertar.json")
        frameActual = context.scene.frame_current
        listaInsertado = list()

        if dataInsertar is None:
            self.report({"INFO"}, f"No información de insertar .config/pluginBlenderALSW/data/insertar.json")
            mostrarMensajeBox("No información de insertar config/pluginBlenderALSW/data/aninsertarimar.json", title="Error", icon="ERROR")

            return {"FINISHED"}

        for insertar in dataInsertar:
            archivo = insertar.get("archivo")
            desface = int(insertar.get("desface", 0) * framerate)
            duracion = int(insertar.get("duracion", 3) * framerate)
            canal = insertar.get("canal", 1)

            if archivo is None:
                self.report({"INFO"}, f"Error no se encontró archivo")
                continue

            if not os.path.exists(archivo):
                self.report({"INFO"}, f"El archivo {archivo} no existe")
                mostrarMensajeBox(f"El archivo {archivo} no existe", title="Error", icon="ERROR")
                continue

            tipo = archivo.split(".")[-1].lower()

            if tipo in ["jpg", "jpeg", "bmp", "png", "gif", "tga", "tiff"]:
                self.report({"INFO"}, f"Insertando Imagen {tipo} - {frameActual + desface}")
                archivoImagen = archivo.split("/")[-1]
                folderImagen = archivo.split("/")
                folderImagen = folderImagen[:-1]
                folderImagen = "/".join(folderImagen) + "/"
                bpy.ops.sequencer.image_strip_add(
                    directory=folderImagen,
                    files=[{"name": archivoImagen, "name": archivoImagen}],
                    frame_start=frameActual + desface,
                    frame_end=frameActual + desface + duracion,
                    channel=canal,
                )
            elif tipo in ["acc", "ac3", "flac", "mp2", "mp3", "m4a", "pcm", "ogg"]:
                self.report({"INFO"}, f"Insertando Audio {tipo} - {frameActual + desface}")
                bpy.ops.sequencer.sound_strip_add(
                    filepath=archivo,
                    frame_start=frameActual + desface,
                    channel=canal
                )
            elif tipo in ["avi", "mp4", "mpg", "mpeg", "mov", "mkv", "dv", "flv"]:
                self.report({"INFO"}, f"Insertando Video {tipo} - {frameActual + desface}")
                bpy.ops.sequencer.movie_strip_add(
                    filepath=archivo,
                    frame_start=frameActual + desface,
                    channel=canal
                )
            else:
                self.report({"INFO"}, f"No se puede insertar {tipo}")

            for secuencia in context.selected_sequences:
                listaInsertado.append(secuencia.name)
                for atributos in insertar:
                    if atributos in ["archivo", "desface", "duracion", "canal"]:
                        continue

                    propiedad = atributos
                    valor = insertar.get(atributos)

                    if valor is not None:
                        if "rotation" in propiedad:
                            valor = valor * (pi / 180)
                        if asignarDinámica(secuencia, propiedad, valor):
                            self.report({"INFO"}, f"Propiedad[{propiedad}] {valor}")
                        else:
                            self.report({"INFO"}, f"Error[{propiedad}] {valor}")

        for secuencia in context.scene.sequence_editor.sequences_all:
            for insertados in listaInsertado:
                if secuencia.name == insertados:
                    secuencia.select = True

        return {"FINISHED"}
