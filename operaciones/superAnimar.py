import bpy

from .FuncionesArchivos import ObtenerArchivo
from .extras import mostrarMensajeBox
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
        frameCursor = context.scene.frame_current

        self.report({"INFO"}, f"Insertando Animación")
        dataAnimación = ObtenerArchivo("data/animar.json")

        if dataAnimación is None:
            self.report({"INFO"}, f"No informacion de animacion .config/pluginBlenderALSW/data/animar.json")
            mostrarMensajeBox("No informacion de animacion .config/pluginBlenderALSW/data/animar.json", title="Error", icon="ERROR")

            return {"FINISHED"}

        for secuencia in context.selected_sequences:
            self.report({"INFO"}, f"Animando {secuencia.name} ")

            frameAnterior = secuencia.frame_final_start

            for keyFrame in dataAnimación:
                frame = None

                inicio = keyFrame.get("inicio")
                final = keyFrame.get("final")
                cursor = keyFrame.get("cursor")
                mover = keyFrame.get("mover")

                if inicio is not None:
                    if isinstance(inicio, str):
                        inicio = float(inicio.replace('%', ''))/100
                        inicio = int(inicio * (secuencia.frame_final_end - secuencia.frame_final_start))
                        frame = secuencia.frame_final_start + inicio
                    else:
                        frame = secuencia.frame_final_start + int(inicio * framerate)
                elif final is not None:
                    if isinstance(final, str):
                        final = float(final.replace('%', ''))/100
                        final = int(final* (secuencia.frame_final_end - secuencia.frame_final_start))
                        frame = secuencia.frame_final_end + final
                    else:
                        frame = secuencia.frame_final_end + int(final * framerate)
                elif cursor is not None:
                    frame = frameCursor + int(cursor * framerate)
                elif mover is not None:
                    frame = frameAnterior + int(mover * framerate)

                for propiedades in keyFrame:
                    if propiedades in ["inicio", "final", "cursor", "mover"]:
                        continue

                    propiedad = propiedades
                    valor = keyFrame.get(propiedades)

                    if propiedad is None:
                        continue

                    if valor is not None:
                        self.report({"INFO"}, f"Asignar[{propiedad}] {valor}")
                        asignarDinámica(secuencia, propiedad, valor)

                    objetoAnimar = obtenerObjetoAtributo(secuencia, propiedad)
                    propiedadAnimar = propiedad.split('.')[-1]

                    if frame is None:
                        objetoAnimar.keyframe_insert(data_path=propiedadAnimar)
                        self.report({"INFO"}, f"Animando[{propiedadAnimar}]")
                    else:
                        objetoAnimar.keyframe_insert(data_path=propiedadAnimar, frame=frame)
                        self.report({"INFO"}, f"Animando[{propiedadAnimar}] {frame}")

                frameAnterior = frame

        return {"FINISHED"}
