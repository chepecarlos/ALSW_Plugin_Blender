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

        archivoSutitulo = os.path.join(folder, "subtitulo.csv")

        return os.path.exists(archivoSutitulo)

    def execute(self, context):

        scene = context.scene
        seq = scene.sequence_editor
        secuencias = seq.sequences_all
        render = context.scene.render
        framerate = render.fps / render.fps_base

        folder = os.path.dirname(bpy.data.filepath)

        archivoSubtitulo = os.path.join(folder, "subtitulo.csv")

        if not os.path.exists(archivoSubtitulo):
            self.report({"INFO"}, f"No Existe el archivo subtitulos.csv")
            return {"FINISHED"}

        archivoData = "data/blender_subtitulo.json"
        x = ObtenerValor(archivoData, "x")
        y = ObtenerValor(archivoData, "y")
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

        with open(archivoSubtitulo) as dataSubtitulo:
            dataCSV = csv.reader(dataSubtitulo, delimiter=",")
            listaLineas = []
            for linea in dataCSV:
                listaLineas.append(linea)

            for linea in listaLineas:
                linea[0] = trasformarFrame(linea[0], framerate)
                linea[1] = trasformarFrame(linea[1], framerate)

            for id, linea in enumerate(listaLineas[:-1]):
                if listaLineas[id][1] > listaLineas[id + 1][0]:
                    listaLineas[id][1] = listaLineas[id + 1][0]

            for lineas in listaLineas:
                inicio = lineas[0]
                Final = lineas[1]
                Mensaje = lineas[2]

                bpy.ops.sequencer.effect_strip_add(type="TEXT", frame_start=inicio, frame_end=Final, channel=5)

                clipActual = context.selected_sequences[0]
                clipActual.name = f"{prefijo}{Mensaje}"
                clipActual.text = Mensaje
                clipActual.font_size = tamanno
                clipActual.use_box = True
                clipActual.align_x = "LEFT"
                clipActual.align_y = "TOP"
                clipActual.use_bold = True

                clipActual.location = (x, y)
                clipActual.color = t_color
                clipActual.wrap_width = 1
                clipActual.box_color = f_color
                clipActual.color_tag = "COLOR_08"

                self.report({"INFO"}, f"Inicio: {inicio} Final: {Final} Mensaje: {Mensaje}")

        self.report({"INFO"}, f"Folder actual {folder}")

        return {"FINISHED"}


def trasformarFrame(tiempo, frame):
    h, m, s = tiempo.split(":")
    return int((int(h) * 3600 + int(m) * 60 + float(s)) * frame)
