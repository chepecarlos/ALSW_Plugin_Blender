import bpy


class preEditar(bpy.types.Operator):
    bl_idname = "scene.preeditar"
    bl_label = "Pre-Editar"
    bl_description = "Iniciar pre-edicion"

    def execute(self, context):
        return {"FINISHED"}
