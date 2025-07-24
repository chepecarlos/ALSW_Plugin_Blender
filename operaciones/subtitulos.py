import csv
import os
import json


import bpy
import blf

from .FuncionesArchivos import ObtenerArchivo
from .funcionesExtras import asignarDinámica, cargarFuente
from .extras import mostrarMensajeBox


class subtitulo(bpy.types.Operator):
    bl_idname = "scene.subtitulo"
    bl_label = "Subtitulo"
    bl_description = "Inserta los Subtítulos desde un archivo subtitulo/out.json"
    bl_options = {"REGISTER", "UNDO"}
    # TODO: quitar puntos si se incluyen en texto

    @classmethod
    def poll(cls, context):
        
        folder = os.path.dirname(bpy.data.filepath)
        nombreArchivo = os.path.splitext(os.path.basename(bpy.data.filepath))[0]
        folderSubtitulos = f"{folder}/subtitulo_{nombreArchivo}"
        archivoSubtitulo = f"{folderSubtitulos}/out.json"

        return os.path.exists(archivoSubtitulo)

    def execute(self, context):
        # TODO: problema con números con decimales

        scene = context.scene
        seq = scene.sequence_editor
        secuencias = seq.sequences_all
        render = context.scene.render
        frameFinal = context.scene.frame_end
        frameInicio = context.scene.frame_start
        framerate = render.fps / render.fps_base
        anchoPantalla = context.scene.render.resolution_x

        # Quitar subtítulos anteriores
        prefijo = "subtitulo."
        for secuencia in secuencias:
            Titulo = secuencia.name
            if Titulo.startswith(prefijo):
                seq.sequences.remove(secuencia)
        

        archivoData = "data/blender_subtitulo.json"
        propiedadesSubtítulos = ObtenerArchivo(archivoData)
        if propiedadesSubtítulos is None:
            self.report({"INFO"}, f"No existe el archivo {archivoData}")
            mostrarMensajeBox("No existe el archivo {archivoData}", title="Error", icon="ERROR")
            return {"FINISHED"}

        archivoDataResaltado = "data/blender_subtitulo_resaltado.json"
        propiedadesSubtítulosResaltado = ObtenerArchivo(archivoDataResaltado)
        if propiedadesSubtítulosResaltado is None:
            self.report({"INFO"}, f"No existe el archivo {archivoDataResaltado}")
            mostrarMensajeBox("No existe el archivo {archivoDataResaltado}", title="Error", icon="ERROR")
            return {"FINISHED"}

        archivoExtra = "data/blender_subtitulo_extra.json"
        propiedadesSubtítulosExtra = ObtenerArchivo(archivoExtra)
        if propiedadesSubtítulosExtra is None:
            self.report({"INFO"}, f"No existe el archivo {archivoExtra}")
            mostrarMensajeBox("No existe el archivo {archivoData}", title="Error", icon="ERROR")
            return {"FINISHED"}

        urlFuente = propiedadesSubtítulosExtra.get("fuente")
        archivoFuente = os.path.basename(urlFuente)

        idFuenteSelection, idFuente = cargarFuente(urlFuente)

        idFuente = blf.load(urlFuente)
        self.report({"INFO"}, f"Fuente seleccionada: {archivoFuente}:{idFuente} URL: {urlFuente}")

        self.report({"INFO"}, f"Propiedades subtitulo {propiedadesSubtítulos}")

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


        palabrasPorLinea = propiedadesSubtítulosExtra.get("palabras_linea", 1)

        segmentos = dataSubtitulo.get("segments", [])
        tamañoFuente = propiedadesSubtítulos.get("font_size", 100)

        lineasPalabras = list()
        palabrasActuales = list()
        fraseActual = ""
        contadorPalabras = 0

        for linea in segmentos:
            palabras = linea.get("words", [])

            palabraAnterior = None

            for palabra in palabras:
                mensaje = palabra.get("word", "")

                fraseActual = ""

                for palabraActual in palabrasActuales:
                    mensajeActual = palabraActual.get("word", "")
                    mensajeActual = mensajeActual.strip()
                    fraseActual += mensajeActual + " "

                fraseActual += mensaje.strip()
                fraseActual = fraseActual.strip()
                fraseActual = fraseActual.capitalize()

                anchoFraseActual = self.calcularAnchoFrase(fraseActual, idFuente, tamañoFuente)

                esperaCorte = propiedadesSubtítulosExtra.get("espera", 0.4)

                if palabraAnterior is not None:
                    tiempoFinPalabraAnterior = palabraAnterior.get("end", 0)
                    tiempoInicioPalabra = palabra.get("start", 0)
                    if tiempoInicioPalabra - tiempoFinPalabraAnterior >= esperaCorte:
                        self.report({"INFO"}, f"Corte: {mensaje.strip()} {tiempoInicioPalabra} - {tiempoFinPalabraAnterior}: {tiempoInicioPalabra - tiempoFinPalabraAnterior}")
                        palabraAnterior = None
                        contadorPalabras = 0
                        lineasPalabras.append(palabrasActuales)
                        palabrasActuales = list()
                        palabrasActuales.append(palabra)
                        continue

                if anchoFraseActual > anchoPantalla * 0.9:
                    palabraAnterior = None
                    contadorPalabras = 0
                    lineasPalabras.append(palabrasActuales)
                    palabrasActuales = list()
                    palabrasActuales.append(palabra)
                    continue

                palabrasActuales.append(palabra)
                palabraAnterior = palabra
                contadorPalabras += 1

                if contadorPalabras >= palabrasPorLinea:
                    contadorPalabras = 0
                    palabraAnterior = None
                    lineasPalabras.append(palabrasActuales)
                    palabrasActuales = list()

        for linea in lineasPalabras:
            contadorPalabras = 0
            frase = ""

            for palabra in linea:
                mensaje = palabra.get("word", "")
                frase = frase + mensaje
            frase = frase.strip()
            frase = frase.capitalize()

            primeraPalabra = linea[0]
            ultimaPalabra = linea[-1]
            inicioFrase = primeraPalabra.get("start", 0)
            finalFrase = ultimaPalabra.get("end", 0)

            inicio = trasformarFrame(inicioFrase, framerate) + frameInicio
            final = trasformarFrame(finalFrase, framerate) + frameInicio
            if final > frameFinal:
                final = frameFinal

            bpy.ops.sequencer.effect_strip_add(type="TEXT", frame_start=inicio, frame_end=final, channel=10)
            clipActual = context.selected_sequences[0]
            # TODO; revisar problema con nombre con numeros
            clipActual.name = f"{prefijo}{frase}"
            clipActual.text = frase.capitalize()
            clipActual.color_tag = "COLOR_08"
            clipActual.font = bpy.data.fonts[idFuenteSelection]

            anchoFrase = self.calcularAnchoFrase(frase.capitalize(), idFuente, tamañoFuente)

            for propiedad, valor in propiedadesSubtítulos.items():
                asignarDinámica(clipActual, propiedad, valor)

            fraseAnterior = ""
            contadorInterno = 0
            for palabra in linea:
                inicioPalabra = palabra.get("start", 0)
                finalPalabra = palabra.get("end", 0)
                mensaje = palabra.get("word", "")
                mensaje = mensaje.strip()

                inicioPalabra = trasformarFrame(inicioPalabra, framerate) + frameInicio
                finalPalabra = trasformarFrame(finalPalabra, framerate) + frameInicio
                if final > frameFinal:
                    final = frameFinal
                if inicioPalabra == finalPalabra:
                    self.report({"INFO"}, f"Ignorar: {mensaje} - {palabra.get('start', 0)} - {palabra.get('end', 0)}")
                if contadorInterno == 0:
                    mensaje = mensaje.capitalize()
                    contadorInterno += 1

                if inicioPalabra != finalPalabra:
                    bpy.ops.sequencer.effect_strip_add(type="TEXT", frame_start=inicioPalabra, frame_end=finalPalabra, channel=11)

                    clipActual = context.selected_sequences[0]
                    clipActual.name = f"{prefijo}{mensaje}"

                    clipActual.text = mensaje
                    clipActual.color_tag = "COLOR_08"
                    clipActual.font = bpy.data.fonts[idFuenteSelection]

                    for propiedad, valor in propiedadesSubtítulos.items():
                        asignarDinámica(clipActual, propiedad, valor)

                    for propiedad, valor in propiedadesSubtítulosResaltado.items():
                        asignarDinámica(clipActual, propiedad, valor)

                    if mensaje.startswith("."):
                        fraseAnterior = fraseAnterior.strip()

                    anchoPalabra = self.calcularAnchoFrase(mensaje, idFuente, tamañoFuente)
                    anchoAnterior = self.calcularAnchoFrase(fraseAnterior, idFuente, tamañoFuente)

                    posiciónX = (-anchoFrase + anchoPalabra) / 2 + anchoAnterior
                    clipActual.transform.offset_x = posiciónX

                fraseAnterior += mensaje + " "

        return {"FINISHED"}

    def calcularAnchoFrase(self, mensaje, idFuente, tamañoFuente):
        blf.size(idFuente, tamañoFuente)
        anchoFrase, altoFrase = blf.dimensions(idFuente, mensaje)
        return anchoFrase


def trasformarFrame(tiempo, frame):

    return int(float(tiempo) * frame)

    # h, m, s = tiempo.split(":")
    # return int((int(h) * 3600 + int(m) * 60 + float(s)) * frame)
