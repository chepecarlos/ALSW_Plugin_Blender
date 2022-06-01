import bpy
from pathlib import Path

from bpy.props import (
    BoolProperty,
    FloatProperty,
    EnumProperty,
    IntProperty,
)

from .FuncionesArchivos import ObtenerValor, SalvarValor

archivoIndice = "1.Guion/4.Indice.md"


class autoanotar(bpy.types.Operator):
    bl_idname = "scene.autoanotar"
    bl_label = "Inserta Anotaciones"
    bl_description = "Inserta la anotación en base archivo"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        archivoFuente = context.blend_data.filepath
        folderProyecto = Path(archivoFuente).parent.parent
        archivo = folderProyecto.joinpath(archivoIndice)
        return archivo.is_file()

    def execute(self, context):
        prefijo = ">Clip-"
        archivoFuente = context.blend_data.filepath
        folderProyecto = Path(archivoFuente).parent.parent
        archivo = folderProyecto.joinpath(archivoIndice)
        sorted_markers = sorted(
            context.scene.timeline_markers, key=lambda m: m.frame)

        for marker in sorted_markers:
            if marker.name.startswith(prefijo):
                context.scene.timeline_markers.remove(marker)

        if not archivo.is_file():
            self.report({"INFO"}, f"No existe el Archivo: {archivoIndice}")
            return {"CANCELLED"}
        
        render = context.scene.render


        titulo_prefijo = "  - title: "
        tiempo_prefijo = "    time: \""
        framerate = render.fps / render.fps_base

        lineas = None
        with open(archivo) as f:
            lineas = f.readlines()

        if lineas is not None:
            print("Empezando a Analizar:")
            titulo = None
            id = 1
            for linea in lineas:

                if linea.startswith(titulo_prefijo):
                    titulo = linea.replace(titulo_prefijo, "")
                    titulo = titulo.replace("\n", "")
                    titulo = f"{prefijo}{id} {titulo}"
                    id += 1

                if linea.startswith(tiempo_prefijo):
                    tiempo = linea.replace(tiempo_prefijo, "")
                    tiempo = tiempo.replace("\"\n", "")

                    tiempoSplit = tiempo.split(":")
                    segundos = int(tiempoSplit[-1])
                    if len(tiempoSplit) > 1:
                        segundos += int(tiempoSplit[-2]) * 60
                    if len(tiempoSplit) > 2:
                        segundos += int(tiempoSplit[-3]) * 3600
                    frame = segundos * framerate
                    self.report({"INFO"}, f"Clip: {tiempo}({frame})-{titulo}")
                    context.scene.frame_current = int(frame)
                    bpy.ops.marker.add()
                    bpy.ops.marker.rename(name=titulo)

        return{'FINISHED'}
