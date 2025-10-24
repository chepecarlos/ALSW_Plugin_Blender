import csv
import os
import json

import bpy

from .extras import mostrarMensajeBox


class palabraPorMinuto(bpy.types.Operator):
    bl_idname = "scene.ppm"
    bl_label = "palabraporminuto"
    bl_description = "Calcula la palabra por minutos"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):

        folder = os.path.dirname(bpy.data.filepath)
        nombreArchivo = os.path.splitext(os.path.basename(bpy.data.filepath))[0]
        folderSubtitulos = f"{folder}/subtitulo_{nombreArchivo}"
        archivoSubtitulo = f"{folderSubtitulos}/out.json"

        return os.path.exists(archivoSubtitulo)

    def execute(self, context):

        folder = os.path.dirname(bpy.data.filepath)
        nombreArchivo = os.path.splitext(os.path.basename(bpy.data.filepath))[0]
        folderSubtitulos = f"{folder}/subtitulo_{nombreArchivo}"
        archivoSubtitulo = f"{folderSubtitulos}/out.json"

        if not os.path.exists(archivoSubtitulo):
            mostrarMensajeBox(f"No Existe el archivo {archivoSubtitulo}", title="Error", icon="ERROR")
            self.report({"INFO"}, f"No Existe el archivo {archivoSubtitulo}")
            return {"FINISHED"}

        dataSubtitulo = None
        with open(archivoSubtitulo) as f:
            dataSubtitulo = json.load(f)

        segmentos = dataSubtitulo.get("segments", [])

        cantidadPalabras: int = 0

        for linea in segmentos:
            palabras = linea.get("words", [])

            for palabra in palabras:
                mensaje = palabra.get("word", "")
                cantidadPalabras += 1
                self.report({"INFO"}, f"{cantidadPalabras} - {mensaje.strip()}")

        self.report({"INFO"}, f"Cantidad total de palabras: {cantidadPalabras}")

        frameFinal = context.scene.frame_end
        frameInicio = context.scene.frame_start
        frameVideo = frameFinal - frameInicio

        render = context.scene.render
        framerate = render.fps / render.fps_base

        duracionVideo = frameVideo / framerate

        self.report({"INFO"}, f"Duración video: {duracionVideo:.2f} Segundos")

        ppm = cantidadPalabras / (duracionVideo/60)
        
        self.report({"INFO"}, f"Palabra por Minuto: {ppm:.2f}")
        
        mostrarMensajeBox(f"Palabra por Minuto: {ppm:.2f}")

        return {"FINISHED"}
