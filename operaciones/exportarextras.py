import datetime as dt
from operator import attrgetter

import bpy
from bpy.props import BoolProperty, EnumProperty, FloatProperty, IntProperty

from .extras import MostarMensajeBox
from .FuncionesArchivos import ObtenerValor, SalvarValor


class exportarextra(bpy.types.Operator):
    bl_idname = "scene.exportarextra"
    bl_label = "Exporta indice extra"
    bl_description = "copia a papelera los indice extras"
    bl_options = {"REGISTER", "UNDO"}

    prefijo: EnumProperty(
        name="prefijo del indice",
        description="Prefijo a buscar",
        items=(
            ("link", "Links >L", "Link de referencia de los videos"),
            ("tarjeta", "Tarjetas >T", "Tarjetas que se pones esquina derecha del video"),
            ("video", "Videos >V", "Video que se mencioan en el video"),
            ("ads", "Ads >A", "Publicidad del video"),
            ("credito", "Creditos >C", "Credito a contenido usando en el video"),
            ("pantalla", "Pantalla Final >P", "Pantalla final del video"),
            ("recursos", "Recursos de Edición >R", "Recursos de Edición"),
            ("notas", "Notas de Edición >R", "Notas de Edicion"),
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
        PrimerIndice = None
        for marker in sorted_markers:

            Titulo = marker.name
            Encontrado = False
            Prefijo = ""

            if PrimerIndice is None:
                PrimerIndice = marker.frame

            if self.prefijo == "link":
                Prefijo = ">L "
                if Titulo.startswith(Prefijo):
                    markers_as_timecodes.append(ExpoertarLinks(Prefijo, Titulo))
                Encontrado = True
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
            elif self.prefijo == "recursos":
                Prefijo = ">R "
            elif self.prefijo == "notas":
                Prefijo = ">N "
            Prefijo = Prefijo.lower()

            if Titulo.lower().startswith(Prefijo) and not Encontrado:

                time = dt.datetime(year=1, month=1, day=1) + dt.timedelta(
                    seconds=(marker.frame - PrimerIndice) / framerate
                )
                Tiempo = time.strftime(time_format)
                Titulo = Titulo.replace(Prefijo, "")
                self.report({"INFO"}, f"Encontrado {Tiempo} {Titulo}")
                markers_as_timecodes.append(f"{Tiempo} - {Titulo}")

        if not markers_as_timecodes:
            self.report({"INFO"}, f"No hay {Prefijo} en video")
            MostarMensajeBox(f"No hay {Prefijo} en video", title="Error", icon="ERROR")
            return {"CANCELLED"}

        bpy.context.window_manager.clipboard = "\n".join(markers_as_timecodes)

        return {"FINISHED"}


def ExpoertarLinks(Prefijo, Titulo):
    Titulo = Titulo.replace(Prefijo, "")
    Titulo = Titulo.split("-")

    title = Titulo[0]

    if len(Titulo) < 2:
        return f"  - title: {title}\n"

    url = Titulo[1]
    return f"  - title: {title}\n    url: {url}"
