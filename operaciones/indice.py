from operator import attrgetter

import bpy
from bpy.props import BoolProperty, EnumProperty, FloatProperty, IntProperty

from .FuncionesArchivos import ObtenerValor, SalvarValor, ObtenerArchivo
from .extras import mostrarMensajeBox
from .funcionesExtras import asignarDinámica, cargarFuente


class superindice(bpy.types.Operator):
    bl_idname = "scene.superindice"
    bl_label = "Generdor Indices"
    bl_description = "Agrega Markas como Texto en el video"
    bl_options = {"REGISTER", "UNDO"}

    Duracion: FloatProperty(name="duracion", description="duracion indice", default=1, min=0)

    @classmethod
    def poll(cls, context):
        return context.scene.timeline_markers

    def execute(self, context):

        indices = context.scene.timeline_markers
        scene = context.scene
        seq = scene.sequence_editor
        secuencias = seq.sequences_all
        render = context.scene.render
        framerate = render.fps / render.fps_base

        if indices is None:
            return {"CANCELLED"}
        indices = sorted(indices, key=attrgetter("frame"))
        indices = indices[1:]

        dataIndice = ObtenerArchivo("data/indice.json")

        if dataIndice is None:
            self.report({"INFO"}, f"No informacion de animacion .config/pluginBlenderALSW/data/indice.json")
            mostrarMensajeBox("No informacion de animacion .config/pluginBlenderALSW/data/indice.json", title="Error", icon="ERROR")

            return {"FINISHED"}

        dataIndiceExtra = ObtenerArchivo("data/indice_extra.json")

        if dataIndiceExtra is None:
            self.report({"INFO"}, f"No informacion de animacion .config/pluginBlenderALSW/data/indice_extra.json")
            mostrarMensajeBox("No informacion de animacion .config/pluginBlenderALSW/data/indice_extra.json", title="Error", icon="ERROR")

            return {"FINISHED"}

        fuente = dataIndiceExtra.get("fuente", None)
        tiempoDesaparecer = dataIndiceExtra.get("tiempo_desaparecer", 0.5)
        animaciónDesaparecer = dataIndiceExtra.get("animacion_desaparecer", "OUT")

        prefijo = "indice."

        for secuencia in secuencias:
            Titulo = secuencia.name
            if Titulo.startswith(prefijo):
                self.report({"INFO"}, f"borrar[{Titulo}]")

                seq.sequences.remove(secuencia)

        duraciónIndice = int(dataIndiceExtra.get("duracion", 5) * framerate)
        canal = int(dataIndiceExtra.get("canal", 8))

        for indice in indices:
            Titulo = indice.name
            if not Titulo.startswith(">"):
                frame = indice.frame
                bpy.ops.sequencer.effect_strip_add(type="TEXT", frame_start=frame, frame_end=int(frame + duraciónIndice), channel=canal)
                clipActual = context.selected_sequences[0]
                clipActual.name = f"{prefijo}{Titulo}"
                clipActual.text = Titulo

                if fuente is not None:
                    idFuenteSelection, idFuente = cargarFuente(fuente)
                    clipActual.font = bpy.data.fonts[idFuenteSelection]

                clipActual.color_tag = "COLOR_06"

                for propiedad, valor in dataIndice.items():
                    self.report({"INFO"}, f"probando[{propiedad}] {valor}")
                    if propiedad is None:
                        continue
                    if valor is not None:
                        if asignarDinámica(clipActual, propiedad, valor):
                            self.report({"INFO"}, f"Asignar[{propiedad}] {valor}")

                bpy.ops.sequencer.fades_add(duration_seconds=tiempoDesaparecer, type=animaciónDesaparecer)

        return {"FINISHED"}
