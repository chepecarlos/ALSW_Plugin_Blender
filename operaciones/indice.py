import bpy

from bpy.props import (
    BoolProperty,
    FloatProperty,
    EnumProperty,
    IntProperty,
)
from operator import attrgetter

from .FuncionesArchivos import ObtenerValor, SalvarValor


class superindice(bpy.types.Operator):
    bl_idname = "scene.superindice"
    bl_label = "super indice"
    bl_description = "Agrega texto sobre los indices del video"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.scene.timeline_markers

    def execute(self, context):

        indices = context.scene.timeline_markers

        if indices is None:
            return{'CANCELLED'}
        render = context.scene.render

        framerate = render.fps / render.fps_base

        indice_duracion = ObtenerValor(
            "data/blender.json", "indice_duracion") * framerate
        indice_tamanno = ObtenerValor("data/blender.json", "indice_tamanno")
        indice_x = ObtenerValor("data/blender.json", "indice_x")
        indice_y = ObtenerValor("data/blender.json", "indice_y")

        fade_duracion = ObtenerValor("data/blender.json", "fade_duracion")
        fade_mode = ObtenerValor("data/blender.json", "fade_mode")

        indice_texto_rojo = ObtenerValor(
            "data/blender.json", "indice_texto_rojo")
        indice_texto_azul = ObtenerValor(
            "data/blender.json", "indice_texto_azul")
        indice_texto_verde = ObtenerValor(
            "data/blender.json", "indice_texto_verde")
        indice_texto_alpha = ObtenerValor(
            "data/blender.json", "indice_texto_alpha")
        color_texto = (indice_texto_rojo, indice_texto_verde,
                       indice_texto_azul, indice_texto_alpha)

        indice_box_rojo = ObtenerValor(
            "data/blender.json", "indice_box_rojo")
        indice_box_azul = ObtenerValor(
            "data/blender.json", "indice_box_azul")
        indice_box_verde = ObtenerValor(
            "data/blender.json", "indice_box_verde")
        indice_box_alpha = ObtenerValor(
            "data/blender.json", "indice_box_alpha")
        color_box = (indice_box_rojo, indice_box_verde,
                     indice_box_azul, indice_box_alpha)

        indices = sorted(indices, key=attrgetter("frame"))
        indices = indices[1:]
        for indice in indices:
            texto = indice.name
            frame = indice.frame
            bpy.ops.sequencer.effect_strip_add(
                type='TEXT', frame_start=frame, frame_end=frame+indice_duracion, channel=1)
            clipActual = context.selected_sequences[0]
            clipActual.name = texto
            clipActual.text = texto
            clipActual.font_size = indice_tamanno
            clipActual.use_box = True
            clipActual.align_x = 'LEFT'
            clipActual.align_y = 'TOP'
            clipActual.use_bold = True
            clipActual.location = (indice_x, indice_y)
            clipActual.color = color_texto
            clipActual.box_color = color_box
            bpy.ops.sequencer.fades_add(duration_seconds=fade_duracion, type=fade_mode)

        return {"FINISHED"}
