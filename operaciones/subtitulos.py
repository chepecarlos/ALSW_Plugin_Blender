import csv
import os

import bpy

from .FuncionesArchivos import ObtenerArchivo


class subtitulo(bpy.types.Operator):
    bl_idname = "scene.subtitulo"
    bl_label = "Subtitulo"
    bl_description = "Inserta los Subtítulos desde un archivo subtitulo.sbv"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        folder = os.path.dirname(bpy.data.filepath)
        # TODO: usar el archivo .sbs si existe
        archivoSutitulo = os.path.join(folder, "subtitulo.sbv")

        return os.path.exists(archivoSutitulo)

    def execute(self, context):

        scene = context.scene
        seq = scene.sequence_editor
        secuencias = seq.sequences_all
        render = context.scene.render
        final = context.scene.frame_end
        framerate = render.fps / render.fps_base

        folder = os.path.dirname(bpy.data.filepath)

        archivoSubtitulo = os.path.join(folder, "subtitulo.sbv")

        if not os.path.exists(archivoSubtitulo):
            self.report({"INFO"}, f"No Existe el archivo subtitulo.sbv")
            return {"FINISHED"}

        archivoData = "data/blender_subtitulo.json"
        dataArchivo = ObtenerArchivo(archivoData)

        if dataArchivo is None:
            self.report(
                {"INFO"}, f"No se encontró el archivo Sub .config/pluginBlenderALSW/data/blender_subtitulo.jso")
            dataArchivo = dict()

        x = dataArchivo.get("x", 0.5)
        y = dataArchivo.get("y", 0.5)

        x_aliniacion = dataArchivo.get("x_aliniacion", "CENTER")
        y_aliniacion = dataArchivo.get("y_aliniacion", "TOP")

        tamanno = dataArchivo.get("tamanno", 60)

        t_rojo = dataArchivo.get("t_rojo", 1)
        t_verde = dataArchivo.get("t_verde", 1)
        t_azul = dataArchivo.get("t_azul", 1)
        t_alfa = dataArchivo.get("t_alfa", 1)

        t_color = (t_rojo, t_verde, t_azul, t_alfa)

        f_rojo = dataArchivo.get("f_rojo", 0)
        f_verde = dataArchivo.get("f_verde", 0)
        f_azul = dataArchivo.get("f_azul", 0)
        f_alfa = dataArchivo.get("f_alfa", 0.7)
        f_grosor = dataArchivo.get("f_grosor", 0.03)

        f_color = (f_rojo, f_verde, f_azul, f_alfa)

        b_rojo = dataArchivo.get("b_rojo", 0)
        b_verde = dataArchivo.get("b_verde", 0)
        b_azul = dataArchivo.get("b_azul", 0)
        b_alfa = dataArchivo.get("b_alfa", 0.7)
        b_grosor = dataArchivo.get("b_grosor", 0.6)

        b_color = (b_rojo, b_verde, b_azul, b_alfa)

        canal = dataArchivo.get("canal", 10)

        caja = dataArchivo.get("caja", False)
        borde = dataArchivo.get("borde", False)

        prefijo = "subtitulo."

        for secuencia in secuencias:
            Titulo = secuencia.name
            if Titulo.startswith(prefijo):
                seq.sequences.remove(secuencia)

        inicios = []
        finales = []
        mensajes = []

        with open(archivoSubtitulo) as dataSubtitulo:
            lineas = dataSubtitulo.read()
            lineas = lineas.splitlines()
            for linea in lineas:
                linea = linea.strip()
                if linea == "":
                    continue
                elif "," in linea:
                    numeros = linea.split(",")
                    # TODo erro si un numero incluye coma
                    inicios.append(trasformarFrame(numeros[0], framerate))
                    finales.append(trasformarFrame(numeros[1], framerate))
                    continue
                else:
                    mensajes.append(linea)

        for id, mensaje in enumerate(mensajes[:-1]):
            if finales[id] > inicios[id + 1]:
                finales[id] = inicios[id + 1] - 5

        if finales[-1] > final:
            finales[-1] = final

        inicios[0] = 1

        self.report({"INFO"}, f"Cantidad Sub {len(inicios)} - fps:{framerate}")

        for id, mensaje in enumerate(mensajes):
            inicio = int(inicios[id])
            final = int(finales[id])
            mensaje = mensajes[id]

            self.report(
                {"INFO"}, f"mensaje-{id} {inicio}-{final} \"{mensaje}\"")

            bpy.ops.sequencer.effect_strip_add(type="TEXT", frame_start=int(
                inicio), frame_end=int(final), channel=canal)

            clipActual = context.selected_sequences[0]
            clipActual.name = f"{prefijo}{mensaje}"
            clipActual.text = mensaje
            clipActual.font_size = tamanno

            clipActual.align_x = x_aliniacion
            clipActual.align_y = y_aliniacion
            clipActual.use_bold = True

            clipActual.location = (x, y)
            clipActual.color = t_color
            clipActual.wrap_width = 1

            if caja:
                clipActual.use_box = True
                clipActual.box_color = f_color
                clipActual.box_margin = f_grosor

            if borde:
                clipActual.use_outline = True
                clipActual.box_color = b_color
                clipActual.outline_width = b_grosor

            clipActual.color_tag = "COLOR_08"

        self.report({"INFO"}, f"Folder actual {folder}")

        return {"FINISHED"}


def trasformarFrame(tiempo, frame):

    h, m, s = tiempo.split(":")
    return int((int(h) * 3600 + int(m) * 60 + float(s)) * frame)
