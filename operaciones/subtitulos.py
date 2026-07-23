import csv
import os
import json


import bpy
import blf

from .FuncionesArchivos import ObtenerArchivo, ObtenerFolderConfig
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

        # return True

        return os.path.exists(archivoSubtitulo)

    def execute(self, context):
        # TODO: problema con números con decimales

        scene = context.scene
        seq = scene.sequence_editor
        if seq is None:
            seq = scene.sequence_editor_create()

        if hasattr(seq, "sequences_all"):
            secuencias = list(seq.sequences_all)
            colección_secuencias = seq.sequences
        elif hasattr(seq, "strips_all"):
            secuencias = list(seq.strips_all)
            colección_secuencias = seq.strips
        else:
            secuencias = list(getattr(seq, "sequences", []))
            colección_secuencias = getattr(seq, "sequences", None)
        render = context.scene.render
        frameFinal = context.scene.frame_end
        frameInicio = context.scene.frame_start
        framerate = render.fps / render.fps_base
        anchoPantalla = context.scene.render.resolution_x

        # Quitar subtítulos anteriores
        prefijo = "subtitulo."
        for secuencia in secuencias:
            Titulo = secuencia.name
            if Titulo.startswith(prefijo) and colección_secuencias is not None:
                colección_secuencias.remove(secuencia)

        folder = os.path.dirname(bpy.data.filepath)
        nombreArchivo = os.path.splitext(os.path.basename(bpy.data.filepath))[0]

        folderConfig = ObtenerFolderConfig()
        archivoData = "data/blender_subtitulo.json"
        propiedadesSubtítulos = ObtenerArchivo(archivoData)
        if propiedadesSubtítulos is None:
            rutaCompleta = os.path.join(folderConfig, archivoData)
            self.report({"INFO"}, f"No existe el archivo {rutaCompleta}")
            mostrarMensajeBox(f"No existe el archivo {rutaCompleta}", title="Error", icon="ERROR")
            return {"FINISHED"}

        archivoProyecto = os.path.join(folder, "blender_subtitulo.json")
        if os.path.exists(archivoProyecto):
            with open(archivoProyecto) as f:
                propiedadesSubtítulos.update(json.load(f))
            self.report({"INFO"}, f"Config proyecto aplicada: {archivoProyecto}")

        archivoDataResaltado = "data/blender_subtitulo_resaltado.json"
        propiedadesSubtítulosResaltado = ObtenerArchivo(archivoDataResaltado)
        if propiedadesSubtítulosResaltado is None:
            rutaCompleta = os.path.join(folderConfig, archivoDataResaltado)
            self.report({"INFO"}, f"No existe el archivo {rutaCompleta}")
            mostrarMensajeBox(f"No existe el archivo {rutaCompleta}", title="Error", icon="ERROR")
            return {"FINISHED"}

        archivoResaltadoProyecto = os.path.join(folder, "blender_subtitulo_resaltado.json")
        if os.path.exists(archivoResaltadoProyecto):
            with open(archivoResaltadoProyecto) as f:
                propiedadesSubtítulosResaltado.update(json.load(f))
            self.report({"INFO"}, f"Config resaltado proyecto aplicada: {archivoResaltadoProyecto}")

        archivoExtra = "data/blender_subtitulo_extra.json"
        propiedadesSubtítulosExtra = ObtenerArchivo(archivoExtra)
        if propiedadesSubtítulosExtra is None:
            rutaCompleta = os.path.join(folderConfig, archivoExtra)
            self.report({"INFO"}, f"No existe el archivo {rutaCompleta}")
            mostrarMensajeBox(f"No existe el archivo {rutaCompleta}", title="Error", icon="ERROR")
            return {"FINISHED"}

        archivoExtraProyecto = os.path.join(folder, "blender_subtitulo_extra.json")
        if os.path.exists(archivoExtraProyecto):
            with open(archivoExtraProyecto) as f:
                propiedadesSubtítulosExtra.update(json.load(f))
            self.report({"INFO"}, f"Config extra proyecto aplicada: {archivoExtraProyecto}")

        urlFuente = propiedadesSubtítulosExtra.get("fuente")
        archivoFuente = os.path.basename(urlFuente)

        try:
            idFuenteSelection, idFuente = cargarFuente(urlFuente)
        except FileNotFoundError:
            mostrarMensajeBox(f"No se encontró la fuente:\n{urlFuente}", title="Error de Fuente", icon="ERROR")
            self.report({"ERROR"}, f"Fuente no encontrada: {urlFuente}")
            return {"FINISHED"}

        idFuente = blf.load(urlFuente)
        self.report({"INFO"}, f"Fuente seleccionada: {archivoFuente}:{idFuente} URL: {urlFuente}")

        self.report({"INFO"}, f"Propiedades subtitulo {propiedadesSubtítulos}")
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

        palabraAnterior = None

        for linea in segmentos:
            palabras = linea.get("words", [])

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
                        lineasPalabras.append(palabrasActuales)
                        palabrasActuales = list()
                        palabrasActuales.append(palabra)
                        palabraAnterior = palabra
                        contadorPalabras = 1
                        continue

                if anchoFraseActual > anchoPantalla * 0.9:
                    lineasPalabras.append(palabrasActuales)
                    palabrasActuales = list()
                    palabrasActuales.append(palabra)
                    palabraAnterior = palabra
                    contadorPalabras = 1
                    continue

                palabrasActuales.append(palabra)
                palabraAnterior = palabra
                contadorPalabras += 1

                if contadorPalabras >= palabrasPorLinea:
                    contadorPalabras = 0
                    lineasPalabras.append(palabrasActuales)
                    palabrasActuales = list()

        if palabrasActuales:
            lineasPalabras.append(palabrasActuales)

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

            clipActual = self.agregarTexto(context, inicio, final, 10)
            if clipActual is None:
                self.report({"ERROR"}, "No se pudo crear strip de subtitulo")
                continue
            # TODO; revisar problema con nombre con numeros
            clipActual.name = f"{prefijo}{frase}"
            clipActual.text = frase.capitalize()
            clipActual.color_tag = "COLOR_08"
            clipActual.font = bpy.data.fonts[idFuenteSelection]

            anchoFrase = self.calcularAnchoFrase(frase.capitalize(), idFuente, tamañoFuente)

            for propiedad, valor in propiedadesSubtítulos.items():
                if not asignarDinámica(clipActual, propiedad, valor):
                    self.report({"WARNING"}, f"Propiedad no aplicada: {propiedad} = {valor}")

            fraseAnterior = ""
            contadorInterno = 0
            for palabra in linea:
                inicioPalabra = palabra.get("start", 0)
                finalPalabra = palabra.get("end", 0)
                mensaje = palabra.get("word", "")
                mensaje = mensaje.strip()

                inicioPalabra = trasformarFrame(inicioPalabra, framerate) + frameInicio
                finalPalabra = trasformarFrame(finalPalabra, framerate) + frameInicio
                if finalPalabra > frameFinal:
                    finalPalabra = frameFinal
                if inicioPalabra == finalPalabra:
                    self.report({"INFO"}, f"Ignorar: {mensaje} - {palabra.get('start', 0)} - {palabra.get('end', 0)}")
                if contadorInterno == 0:
                    mensaje = mensaje.capitalize()
                    contadorInterno += 1

                if inicioPalabra != finalPalabra:
                    clipActual = self.agregarTexto(context, inicioPalabra, finalPalabra, 11)
                    if clipActual is None:
                        self.report({"ERROR"}, "No se pudo crear strip de palabra")
                        continue
                    clipActual.name = f"{prefijo}{mensaje}"

                    clipActual.text = mensaje
                    clipActual.color_tag = "COLOR_08"
                    clipActual.font = bpy.data.fonts[idFuenteSelection]

                    for propiedad, valor in propiedadesSubtítulos.items():
                        if not asignarDinámica(clipActual, propiedad, valor):
                            self.report({"WARNING"}, f"Propiedad no aplicada: {propiedad} = {valor}")

                    for propiedad, valor in propiedadesSubtítulosResaltado.items():
                        if not asignarDinámica(clipActual, propiedad, valor):
                            self.report({"WARNING"}, f"Propiedad no aplicada: {propiedad} = {valor}")

                    if mensaje.startswith("."):
                        fraseAnterior = fraseAnterior.strip()

                    anchoPalabra = self.calcularAnchoFrase(mensaje, idFuente, tamañoFuente)
                    anchoAnterior = self.calcularAnchoFrase(fraseAnterior, idFuente, tamañoFuente)

                    posiciónX = (-anchoFrase + anchoPalabra) / 2 + anchoAnterior
                    clipActual.transform.offset_x = posiciónX

                fraseAnterior += mensaje + " "

        return {"FINISHED"}

    def agregarTexto(self, context, inicio, final, canal):
        frameInicio = int(inicio)
        frameFinal = max(frameInicio + 1, int(final))
        duración = max(1, frameFinal - frameInicio)

        seq = context.scene.sequence_editor
        if seq is None:
            seq = context.scene.sequence_editor_create()

        if hasattr(seq, "sequences"):
            colección = seq.sequences
        elif hasattr(seq, "strips"):
            colección = seq.strips
        else:
            return None

        nombreTemporal = f"subtitulo.tmp.{canal}.{frameInicio}"

        try:
            return colección.new_effect(
                name=nombreTemporal,
                type="TEXT",
                channel=canal,
                frame_start=frameInicio,
                frame_end=frameFinal,
            )
        except TypeError:
            try:
                return colección.new_effect(
                    name=nombreTemporal,
                    type="TEXT",
                    channel=canal,
                    frame_start=frameInicio,
                    length=duración,
                )
            except TypeError:
                try:
                    return colección.new_effect(
                        nombreTemporal,
                        "TEXT",
                        canal,
                        frameInicio,
                        frameFinal,
                    )
                except Exception as error:
                    self.report({"ERROR"}, f"Error creando strip: {error}")
                    return None
        except Exception as error:
            self.report({"ERROR"}, f"Error creando strip: {error}")
            return None

    def calcularAnchoFrase(self, mensaje, idFuente, tamañoFuente):
        blf.size(idFuente, tamañoFuente)
        anchoFrase, altoFrase = blf.dimensions(idFuente, mensaje)
        return anchoFrase


def trasformarFrame(tiempo, frame):

    return int(float(tiempo) * frame)

    # h, m, s = tiempo.split(":")
    # return int((int(h) * 3600 + int(m) * 60 + float(s)) * frame)
