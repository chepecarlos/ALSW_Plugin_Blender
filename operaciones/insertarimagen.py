import bpy

from bpy.props import (
    BoolProperty,
    FloatProperty,
    EnumProperty,
    IntProperty,
)

from .FuncionesArchivos import ObtenerValor, SalvarValor
from .extras import MostarMensajeBox


class insertarimagen(bpy.types.Operator):
    bl_idname = "scene.insertarimagen"
    bl_label = "Insertar Clip"
    bl_description = "Insertar imagen en posicion de curso"
    bl_options = {"REGISTER", "UNDO"}

    macros: BoolProperty(name="macro", description="funcion con macro para zoon", default=False)

    @classmethod
    def poll(cls, context):
        return True
        # return context.selected_sequences

    def execute(self, context):


        if self.macros:
            ClipActual = ObtenerValor("data/blender.json", "clip")
            FolderActual = ClipActual.split("/")
            Archivo = FolderActual[-1]
            FolderActual = FolderActual[:-1]
            FolderActual = "/".join(FolderActual)
        else:
            return {"FINISHED"}
        print("Iniciando", ClipActual, FolderActual)

        FrameActual = context.scene.frame_current

        if ClipActual is None:
            MostarMensajeBox("Pista No asignada en: data/blender.json", title="Error", icon="ERROR")
            return {"FINISHED"}

        bpy.ops.sequencer.image_strip_add(
            directory=FolderActual, 
            files=[{"name":Archivo, "name":Archivo}],
            frame_start=FrameActual, frame_end=FrameActual + 60, channel=1)

        return {"FINISHED"}
