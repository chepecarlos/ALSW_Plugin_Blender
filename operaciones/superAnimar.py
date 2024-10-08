import bpy

from .FuncionesArchivos import ObtenerArchivo
from .extras import MostarMensajeBox
from .funcionesExtras import asignarDinámica, obtenerObjetoAtributo, trasformarFrame


class superanimar(bpy.types.Operator):
    bl_idname = "scene.superanimar"
    bl_label = "Animar Clip"
    bl_description = "Anima el clip"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        render = context.scene.render
        framerate = render.fps / render.fps_base

        self.report({"INFO"}, f"Insertando Animación")
        dataAnimación = ObtenerArchivo("data/animar.json")

        if dataAnimación is None:
            self.report(
                {"INFO"}, f"No informacion de animacion config/pluginBlenderALSW/data/animar.json")
            MostarMensajeBox(
                "No informacion de animacion config/pluginBlenderALSW/data/animar.json", title="Error", icon="ERROR")

            return {"FINISHED"}

        for secuencia in context.selected_sequences:
            self.report({"INFO"}, f"Animando {secuencia.name} ")

            frameAnterior = 0

            for keyFrame in dataAnimación:
                frame = None

                propiedad = keyFrame.get("propiedad")
                valor = keyFrame.get("valor")

                tiempo = keyFrame.get("tiempo")
                inicio = keyFrame.get("inicio")
                final = keyFrame.get("final")
                print(keyFrame)

                if propiedad is None:
                    continue

                if valor is not None:
                    self.report({"INFO"}, f"Propiedad[{propiedad}] {valor}")
                    asignarDinámica(secuencia, propiedad, valor)

                # inicio - final
                # ninguna
                # cursor +-
                # avance o mover + -
                if inicio is not None:
                    frame = secuencia.frame_final_start + \
                        int(inicio * framerate)

                if final is not None:
                    frame = secuencia.frame_final_end + \
                        int(final * framerate)

                objetoAnimar = obtenerObjetoAtributo(secuencia, propiedad)
                propiedadAnimar = propiedad.split('.')[-1]
                if frame is None:
                    objetoAnimar.keyframe_insert(data_path=propiedadAnimar)
                else:
                    objetoAnimar.keyframe_insert(
                        data_path=propiedadAnimar, frame=frame)


                print(keyFrame)

        return {"FINISHED"}
