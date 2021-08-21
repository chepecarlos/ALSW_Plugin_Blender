import bpy

from bpy.props import (
    BoolProperty,
    FloatProperty,
    EnumProperty,
    IntProperty,
)

from .FuncionesArchivos import ObtenerValor, SalvarValor

class superaliniar(bpy.types.Operator):
    bl_idname = "scene.superaliniar"
    bl_label = "super Aliniar"
    bl_description = "Alinea los clips"
    bl_options = {"REGISTER", "UNDO"}

    macros: BoolProperty(
        name="macro",
        description="funcion con macro para alinacion",
        default=False
    )

    alineacion_horizontal: EnumProperty(
        name="Alineacion Horizontal de clip",
        description="Alina el clip",
        items=(('derecha', "Derecha", "ALSW base"),
               ('izquierda', "Izquierda", "Musica MrTee"),
               ('centro', "Centro", "musica pollo"),
               ('nada', "Nada", "ninguna")),
        default='nada',)

    alineacion_vertical: EnumProperty(
        name="Alineacion Vertical de clip",
        description="Alina el clip",
        items=(('ariba', "Ariba", "ALSW base"),
               ('abajo', "Abajo", "Musica MrTee"),
               ('centro', "Centro", "musica pollo"),
               ('nada', "Nada", "ninguna")),
        default='nada',)

    # Verifica que este alguna secuencia selecionada
    @classmethod
    def poll(cls, context):
        # Todo: Solo activar con clip de video
        if len(bpy.context.selected_sequences) > 0:
            ClipActual = context.selected_sequences[0]
            if ClipActual.type != "MOVIE" and ClipActual.type != "IMAGE":
                return False
            return context.selected_sequences
        return False

    def execute(self, context):

        if len(bpy.context.selected_sequences) > 0:
            ClipActual = context.selected_sequences[0]
            if ClipActual.type != "MOVIE" and ClipActual.type != "IMAGE":
                return{'FINISHED'}

            if self.macros:
                self.alineacion_vertical = ObtenerValor("data/blender.json", "alineacion_vertical")
                self.alineacion_horizontal = ObtenerValor("data/blender.json", "alineacion_horizontal")
            
            if self.alineacion_vertical is None:
                self.alineacion_vertical = 'nada'

            if self.alineacion_horizontal is None:
                self.alineacion_horizontal = 'nada'

            EsenaActual = context.scene.sequence_editor.active_strip.elements[0]
            AnchoCanva = context.scene.render.resolution_x
            AltoCanva = context.scene.render.resolution_y
            Alto = EsenaActual.orig_height
            Ancho = EsenaActual.orig_width
            # Codigo feo, pero funciona
            if ClipActual.use_proxy:
                # Buscar una forma no sucia
                MultiProxy = ObtenerValor("data/blender.json", "multi_proxy")
                Alto *= MultiProxy
                Ancho *= MultiProxy
            PosicionX = ClipActual.transform.offset_x
            PosicionY = ClipActual.transform.offset_y
            EscalaX = ClipActual.transform.scale_x
            EscalaY = ClipActual.transform.scale_y

            if self.alineacion_vertical == "centro":
                ClipActual.transform.offset_y = 0
            elif self.alineacion_vertical == "ariba":
                AltoClip = Alto * EscalaY
                ValorY = AltoCanva / 2 - AltoClip / 2
                ClipActual.transform.offset_y = ValorY
            elif self.alineacion_vertical == "abajo":
                AltoClip = Alto * EscalaY
                ValorY = AltoCanva / 2 - AltoClip / 2
                ClipActual.transform.offset_y = -ValorY

            if self.alineacion_horizontal == "centro":
                ClipActual.transform.offset_x = 0
            elif self.alineacion_horizontal == "izquierda":
                AnchoClip = Ancho * EscalaX
                ValorX = AnchoCanva / 2 - AnchoClip / 2
                ClipActual.transform.offset_x = -ValorX
            elif self.alineacion_horizontal == "derecha":
                AnchoClip = Ancho * EscalaX
                ValorX = AnchoCanva / 2 - AnchoClip / 2
                ClipActual.transform.offset_x = ValorX
        SalvarValor("data/blender.json", "alineacion_vertical", None)
        SalvarValor("data/blender.json", "alineacion_horizontal", None)
        return{'FINISHED'}

