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


class exportarindice(bpy.types.Operator):
    bl_idname = "scene.exportarindice"
    bl_label = "exporta indice"
    bl_description = "copia a papelera los indice en formado de NocheProgramacion"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.scene.timeline_markers

    def execute(self, context):
        render = context.scene.render

        if len(context.scene.timeline_markers) == 0:
            # TODO Limpiuar codigo en futuro 
            self.report({"INFO"}, "No markers found")
            return {"CANCELLED"}

        sorted_markers = sorted(context.scene.timeline_markers, key=lambda m: m.frame)

        framerate = render.fps / render.fps_base
        last_marker_seconds = sorted_markers[-1].frame / framerate
        seconds_in_hour = 3600.0
        time_format = "%H:%M:%S" if last_marker_seconds >= seconds_in_hour else "%M:%S"

        markers_as_timecodes = []
        PrimerIndice = None
        for marker in sorted_markers:
            Titulo = marker.name

            if not Titulo.startswith(">"):
                
                if PrimerIndice is None:
                    PrimerIndice = marker.frame 

                time = dt.datetime(year=1, month=1, day=1) + dt.timedelta(
                    seconds=(marker.frame - PrimerIndice ) / framerate
                )

                markers_as_timecodes.append("  - title: " + Titulo)
                markers_as_timecodes.append("    time: '" + time.strftime(time_format) + "'")
              
        bpy.context.window_manager.clipboard = "\n".join(markers_as_timecodes)
        return {"FINISHED"}
