import bpy

from bpy.props import (
    BoolProperty,
    FloatProperty,
    EnumProperty,
    IntProperty,
)
from operator import attrgetter
import datetime as dt

from .FuncionesArchivos import ObtenerValor, SalvarValor
from .extras import MostarMensajeBox


class exportarextra(bpy.types.Operator):
    bl_idname = "scene.exportarextra"
    bl_label = "Exporta indice extra"
    bl_description = "copia a papelera los indice extras"
    bl_options = {"REGISTER", "UNDO"}

    prefijo: EnumProperty(
        name="prefijo del indice",
        description="Prefijo a buscar",
        items=(
            ("link", "Links >L", "L"),
            ("tarjeta", "Tarjetas >T", "T"),
            ("video", "Videos >V", "V"),
            ("ads", "Ads >A", "A"),
            ("credito", "Creditos >C", "C"),
            ("pantalla", "Pantalla Final >P", "P"),
        ),
        default="link",
    )

    @classmethod
    def poll(cls, context):
        return context.scene.timeline_markers

    def execute(self, context):
        render = context.scene.render

        if len(context.scene.timeline_markers) == 0:
            self.report({"INFO"}, "No markers found")
            return {"CANCELLED"}

        self.report({"INFO"}, f"El prefijo es {self.prefijo}")

        sorted_markers = sorted(context.scene.timeline_markers, key=lambda m: m.frame)
        framerate = render.fps / render.fps_base
        last_marker_seconds = sorted_markers[-1].frame / framerate
        seconds_in_hour = 3600.0
        time_format = "%H:%M:%S" if last_marker_seconds >= seconds_in_hour else "%M:%S"

        markers_as_timecodes = []
        for marker in sorted_markers:

            Titulo = marker.name

            Prefijo = ""

            if self.prefijo == "link":
                Prefijo = ">L "
            elif self.prefijo == "tarjeta":
                Prefijo = ">T "
            elif self.prefijo == "video":
                Prefijo = ">V"
            elif self.prefijo == "credito":
                Prefijo = ">C "
            elif self.prefijo == "pantalla":
                Prefijo = ">P "
            elif self.prefijo == "ads":
                Prefijo = ">A "

            if Titulo.startswith(Prefijo):

                time = dt.datetime(year=1, month=1, day=1) + dt.timedelta(seconds=marker.frame / framerate)
                Tiempo = time.strftime(time_format)
                Titulo = Titulo.removeprefix(Prefijo)
                self.report({"INFO"}, f"Encontrado {Tiempo} {Titulo}")
                markers_as_timecodes.append(f"Tipo({self.prefijo})")
                markers_as_timecodes.append(Tiempo)
                markers_as_timecodes.append(Titulo)

        if len(markers_as_timecodes) == 0:
            self.report({"INFO"}, f"No hay {Prefijo} en video")
            MostarMensajeBox(f"No hay {Prefijo} en video", title="Error", icon="ERROR")
            return {"CANCELLED"}

        bpy.context.window_manager.clipboard = "\n".join(markers_as_timecodes)

        return {"FINISHED"}
