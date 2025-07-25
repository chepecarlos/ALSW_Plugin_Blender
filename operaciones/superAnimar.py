import bpy
from math import pi

from .FuncionesArchivos import ObtenerArchivo
from .extras import mostrarMensajeBox
from .funcionesExtras import asignarDinámica, cargarFuente, obtenerObjetoAtributo, trasformarFrame


class superanimar(bpy.types.Operator):
    bl_idname = "scene.superanimar"
    bl_label = "Animar Clip"
    bl_description = "Anima el clip"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        # Verifica si hay secuencias seleccionadas
        return True

    def execute(self, context):

        render = context.scene.render
        framerate = render.fps / render.fps_base
        frameCursor = context.scene.frame_current
        escena = context.scene

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
                fuente = keyFrame.get("fuente")
                borrar = keyFrame.get("borrar", False)

                if borrar:
                    nombreSecuencia = secuencia.name
                    action = escena.animation_data.action if escena.animation_data else None
                    if action:

                        for fcurve in list(action.fcurves):

                            if f'sequence_editor.strips_all["{nombreSecuencia}"]' in fcurve.data_path:
                                fcurve.keyframe_points.clear()
                                action.fcurves.remove(fcurve)

                    return {"FINISHED"}  # Si se indica borrar, no se anima nada y se sale de la función

                if inicio is not None:
                    if isinstance(inicio, str):
                        inicio = float(inicio.replace("%", "")) / 100
                        inicio = int(inicio * (secuencia.frame_final_end - secuencia.frame_final_start))
                        frame = secuencia.frame_final_start + inicio
                    else:
                        frame = secuencia.frame_final_start + int(inicio * framerate)
                elif final is not None:
                    if isinstance(final, str):
                        final = float(final.replace("%", "")) / 100
                        final = int(final * (secuencia.frame_final_end - secuencia.frame_final_start))
                        frame = secuencia.frame_final_end + final
                    else:
                        frame = secuencia.frame_final_end + int(final * framerate)
                elif cursor is not None:
                    frame = frameCursor + int(cursor * framerate)
                elif mover is not None:
                    frame = frameAnterior + int(mover * framerate)

                if fuente is not None:
                    idFuenteSelection, idFuente = cargarFuente(fuente)
                    secuencia.font = bpy.data.fonts[idFuenteSelection]

                for propiedades in keyFrame:
                    if propiedades in ["inicio", "final", "cursor", "mover", "fuente"]:
                        continue

                    propiedad = propiedades
                    valor = keyFrame.get(propiedades)

                    if propiedad is None:
                        continue

                    if valor is not None:
                        if "rotation" in propiedad:
                            valor = valor * (pi / 180)
                        if asignarDinámica(secuencia, propiedad, valor):
                            self.report({"INFO"}, f"Asignar[{propiedad}] {valor}")
                        else:
                            self.report({"INFO"}, f"Error[{propiedad}] {valor}")

                    objetoAnimar = obtenerObjetoAtributo(secuencia, propiedad)
                    propiedadAnimar = propiedad.split(".")[-1]

                    if frame is None:
                        objetoAnimar.keyframe_insert(data_path=propiedadAnimar)
                        self.report({"INFO"}, f"Animando[{propiedadAnimar}]")
                    else:
                        objetoAnimar.keyframe_insert(data_path=propiedadAnimar, frame=frame)
                        self.report({"INFO"}, f"Animando[{propiedadAnimar}] {frame}")

                frameAnterior = frame

        return {"FINISHED"}
