import csv
import os

import bpy

from .FuncionesArchivos import ObtenerValor


class subtitulo(bpy.types.Operator):
    bl_idname = "scene.subtitulo"
    bl_label = "Subtitulo"
    bl_description = "Inserta los Subtítulos desde un archivo .csv"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        folder = os.path.dirname(bpy.data.filepath)

        # archivoSutitulo = os.path.join(folder, "subtitulo.csv")
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
            self.report({"INFO"}, f"No Existe el archivo subtitulos.sbv")
            return {"FINISHED"}

        archivoData = "data/blender_subtitulo.json"
        x = ObtenerValor(archivoData, "x")
        y = ObtenerValor(archivoData, "y")

        x_aliniacion = ObtenerValor(archivoData, "x_aliniacion")
        y_aliniacion = ObtenerValor(archivoData, "x_aliniacion")

        tamanno = ObtenerValor(archivoData, "tamanno")

        t_rojo = ObtenerValor(archivoData, "t_rojo")
        t_verde = ObtenerValor(archivoData, "t_verde")
        t_azul = ObtenerValor(archivoData, "t_azul")
        t_alfa = ObtenerValor(archivoData, "t_alfa")

        t_color = (t_rojo, t_verde, t_azul, t_alfa)

        f_rojo = ObtenerValor(archivoData, "f_rojo")
        f_verde = ObtenerValor(archivoData, "f_verde")
        f_azul = ObtenerValor(archivoData, "f_azul")
        f_alfa = ObtenerValor(archivoData, "f_alfa")

        f_color = (f_rojo, f_verde, f_azul, f_alfa)

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
                if linea == "":
                    continue
                elif "," in linea:
                    numeros = linea.split(",")
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

        self.report({"INFO"}, f"cantidad-{len(inicios)}- {framerate}")

        for id, mensaje in enumerate(mensajes):
            inicio = inicios[id]
            final = finales[id]
            mensaje = mensajes[id]

            self.report({"INFO"}, f"mensaje-{id} {inicio}-{final} {mensaje}")

            bpy.ops.sequencer.effect_strip_add(type="TEXT", frame_start=inicio, frame_end=final, channel=5)

            clipActual = context.selected_sequences[0]
            clipActual.name = f"{prefijo}{mensaje}"
            clipActual.text = mensaje
            clipActual.font_size = tamanno

            clipActual.use_box = True
            clipActual.align_x = x_aliniacion
            clipActual.align_y = y_aliniacion
            clipActual.use_bold = True

            clipActual.location = (x, y)
            clipActual.color = t_color
            clipActual.wrap_width = 1
            clipActual.box_color = f_color
            clipActual.box_margin = 0.03

            clipActual.color_tag = "COLOR_08"

        self.report({"INFO"}, f"Folder actual {folder}")

        return {"FINISHED"}


def trasformarFrame(tiempo, frame):
    h, m, s = tiempo.split(":")
    return int((int(h) * 3600 + int(m) * 60 + float(s)) * frame)
