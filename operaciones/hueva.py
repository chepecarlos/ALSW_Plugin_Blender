import datetime as dt

import bpy


class hueva(bpy.types.Operator):
    bl_idname = "scene.hueva"
    bl_label = "Hueva"
    bl_description = "Copia a papelera el tiempo del cursor"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        render = context.scene.render
        framerate = render.fps / render.fps_base
        seconds_in_hour = 3600.0

        FrameActual = context.scene.frame_current
        TiempoActual = FrameActual / framerate

        formatoTiempo = "%H:%M:%S" if TiempoActual >= seconds_in_hour else "%M:%S"

        time = dt.datetime(year=1, month=1, day=1) + dt.timedelta(seconds=TiempoActual)
        extra = round(FrameActual % framerate)

        bpy.context.window_manager.clipboard = f"{time.strftime(formatoTiempo)}+{extra} - {FrameActual} "

        self.report({"INFO"}, f"Cursor en {time.strftime(formatoTiempo)} - {FrameActual}")

        return {"FINISHED"}
