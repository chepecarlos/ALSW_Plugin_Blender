import bpy


class mi_PT_panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window."""

    bl_idname = "MY_PT_mipanel"
    bl_label = "Panel ALSW"
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"

    def draw(self, context):
        """Dibujar el panel."""
        layout = self.layout

        row = layout.row()
        row.label(text="AutoAnotacion")
        ops = row.operator("scene.autoanotar", text="Insertar")

        row = layout.row()
        row.label(text="Poder")
        ops = row.operator("scene.hueva", text="Hueva")

        row = layout.row()
        row.label(text="Subtítulos")
        ops = row.operator("scene.subtitulo", text="Agregar")

        row = layout.row()
        row.label(text="Musica sobre clip", icon="SOUND")
        row = layout.row()
        ops = row.operator("scene.sobreponeraudio", text="MrTee")

        row = layout.row()
        row.label(text="Alineacion")
        row = layout.row()
        ops = row.operator("scene.superaliniar", text="Ariba")
        ops.macros = False
        ops.alineacion_vertical = "ariba"

        row = layout.row()
        ops = row.operator("scene.superaliniar", text="Izquierda")
        ops.macros = False
        ops.alineacion_horizontal = "izquierda"
        ops = row.operator("scene.superaliniar", text="Centro")
        ops.macros = False
        ops.alineacion_horizontal = "centro"
        ops.alineacion_vertical = "centro"
        ops = row.operator("scene.superaliniar", text="Derecha")
        ops.macros = False
        ops.alineacion_horizontal = "derecha"

        row = layout.row()
        ops = row.operator("scene.superaliniar", text="Abajo")
        ops.macros = False
        ops.alineacion_vertical = "abajo"

        row = layout.row()
        row.label(text="Zoon", icon="ZOOM_IN")
        row = layout.row()
        ops = row.operator("scene.superzoon", text="0.25X")
        ops.incrementro = False
        ops.macros = False
        ops.zoon = 0.25
        ops = row.operator("scene.superzoon", text="0.5X")
        ops.incrementro = False
        ops.macros = False
        ops.zoon = 0.5
        ops = row.operator("scene.superzoon", text="0.75X")
        ops.incrementro = False
        ops.macros = False
        ops.zoon = 0.75
        row = layout.row()
        ops = row.operator("scene.superzoon", text="1X")
        ops.incrementro = False
        ops.macros = False
        ops.zoon = 1
        row = layout.row()
        ops = row.operator("scene.superzoon", text="2X")
        ops.incrementro = False
        ops.macros = False
        ops.zoon = 2
        ops = row.operator("scene.superzoon", text="3X")
        ops.incrementro = False
        ops.macros = False
        ops.zoon = 3
        ops = row.operator("scene.superzoon", text="4X")
        ops.incrementro = False
        ops.macros = False
        ops.zoon = 4
        ops = row.operator("scene.superzoon", text="8X")
        ops.incrementro = False
        ops.macros = False
        ops.zoon = 8

        row = layout.row()
        row.label(text="Generador Indice")
        row = layout.row()
        ops = row.operator("scene.superindice", text="Generar")

        row = layout.row()
        row.label(text="Indice para NocheProgramacion")
        row = layout.row()
        ops = row.operator("scene.exportarindice", text="Copiar")

        row = layout.row()
        row.label(text="Exportar Markas Extras")

        row = layout.row()
        ops = row.operator("scene.exportarextra", text="Links")
        ops.prefijo = "link"
        ops = row.operator("scene.exportarextra", text="Tarjetas")
        ops.prefijo = "tarjeta"
        ops = row.operator("scene.exportarextra", text="Videos")
        ops.prefijo = "video"

        row = layout.row()
        ops = row.operator("scene.exportarextra", text="Ads")
        ops.prefijo = "ads"
        ops = row.operator("scene.exportarextra", text="Creditos")
        ops.prefijo = "credito"
        ops = row.operator("scene.exportarextra", text="Pantalla Final")
        ops.prefijo = "pantalla"

        row = layout.row()
        ops = row.operator("scene.exportarextra", text="Recursos")
        ops.prefijo = "recursos"
        ops = row.operator("scene.exportarextra", text="Notas")
        ops.prefijo = "notas"
