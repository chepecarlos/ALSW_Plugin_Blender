import json
import os

import bpy

from .FuncionesArchivos import ObtenerArchivo
from .subtitulos import trasformarFrame


class preEditar(bpy.types.Operator):
    bl_idname = "scene.preeditar"
    bl_label = "Pre-Editar"
    bl_description = "Iniciar pre-edicion"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        folder = os.path.dirname(bpy.data.filepath)
        nombreArchivo = os.path.splitext(os.path.basename(bpy.data.filepath))[0]
        folderSubtitulos = f"{folder}/subtitulo_{nombreArchivo}"
        archivoSubtitulo = f"{folderSubtitulos}/out.json"

        return os.path.exists(archivoSubtitulo)

    def execute(self, context):
        scene = context.scene
        render = scene.render
        framerate = render.fps / render.fps_base
        frameInicio = scene.frame_start
        frameFinal = scene.frame_end

        folder = os.path.dirname(bpy.data.filepath)
        nombreArchivo = os.path.splitext(os.path.basename(bpy.data.filepath))[0]
        folderSubtitulos = f"{folder}/subtitulo_{nombreArchivo}"
        archivoSubtitulo = f"{folderSubtitulos}/out.json"

        with open(archivoSubtitulo) as f:
            dataSubtitulo = json.load(f)

        palabras = []
        for segmento in dataSubtitulo.get("segments", []):
            palabras.extend(segmento.get("words", []))
        palabras.sort(key=lambda palabra: palabra.get("start", 0))

        if not palabras:
            self.report({"INFO"}, "No hay palabras en out.json")
            return {"FINISHED"}

        propiedades = ObtenerArchivo("data/pre_editar.json") or {}
        archivoProyecto = os.path.join(folder, "blender_pre_editar.json")
        if os.path.exists(archivoProyecto):
            with open(archivoProyecto) as f:
                propiedades.update(json.load(f))

        umbralSilencio = propiedades.get("umbral_silencio", 1.0)
        margen = propiedades.get("margen", 0.15)
        colorEtiqueta = propiedades.get("color", "COLOR_01")

        # Cada hueco indica si su borde linda con una palabra hablada (y por
        # lo tanto necesita el margen de seguridad) o con el borde del
        # timeline (donde no hay nada que proteger).
        huecos = []

        primeraPalabra = palabras[0]
        inicioPrimera = primeraPalabra.get("start", 0)
        if inicioPrimera >= umbralSilencio:
            huecos.append((0, inicioPrimera, False, True))

        for anterior, actual in zip(palabras, palabras[1:]):
            fin = anterior.get("end", 0)
            inicio = actual.get("start", 0)
            if inicio - fin >= umbralSilencio:
                huecos.append((fin, inicio, True, True))

        ultimaPalabra = palabras[-1]
        finUltima = ultimaPalabra.get("end", 0)
        duraciónTimeline = (frameFinal - frameInicio) / framerate
        if duraciónTimeline - finUltima >= umbralSilencio:
            huecos.append((finUltima, duraciónTimeline, True, False))

        if not huecos:
            self.report({"INFO"}, "No se encontraron silencios")
            return {"FINISHED"}

        rangosFrame = []
        for inicioHueco, finHueco, margenInicio, margenFin in huecos:
            inicioConMargen = inicioHueco + margen if margenInicio else inicioHueco
            finConMargen = finHueco - margen if margenFin else finHueco
            if finConMargen <= inicioConMargen:
                continue
            frameHuecoInicio = trasformarFrame(inicioConMargen, framerate) + frameInicio
            frameHuecoFin = trasformarFrame(finConMargen, framerate) + frameInicio
            rangosFrame.append((frameHuecoInicio, frameHuecoFin))

        if not rangosFrame:
            self.report({"INFO"}, "No quedaron silencios tras aplicar el margen")
            return {"FINISHED"}

        seq = scene.sequence_editor
        if seq is None:
            self.report({"INFO"}, "No hay secuenciador")
            return {"FINISHED"}

        for frameHuecoInicio, frameHuecoFin in rangosFrame:
            bpy.ops.sequencer.split(frame=frameHuecoInicio, type="SOFT", ignore_selection=True)
            bpy.ops.sequencer.split(frame=frameHuecoFin, type="SOFT", ignore_selection=True)

        if hasattr(seq, "strips_all"):
            secuencias = list(seq.strips_all)
        elif hasattr(seq, "sequences_all"):
            secuencias = list(seq.sequences_all)
        else:
            secuencias = []

        contadorSeleccionados = 0
        for secuencia in secuencias:
            secuencia.select = False
            for frameHuecoInicio, frameHuecoFin in rangosFrame:
                if secuencia.frame_final_start >= frameHuecoInicio and secuencia.frame_final_end <= frameHuecoFin:
                    secuencia.select = True
                    contadorSeleccionados += 1
                    break

        if contadorSeleccionados > 0:
            try:
                bpy.ops.sequencer.strip_color_tag_set(color=colorEtiqueta)
            except Exception as error:
                self.report({"WARNING"}, f"No se pudo aplicar color: {error}")

        self.report(
            {"INFO"},
            f"{len(rangosFrame)} silencios encontrados, {contadorSeleccionados} clips seleccionados",
        )
        return {"FINISHED"}
