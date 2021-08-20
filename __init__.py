import bpy

bl_info = {
    "name": "ALSW_Plugin_Blender",
    "author": "ChepeCarlos",
    "description": "Heramientas Extra para Sequencer",
    "blender": (2, 80, 0),
    "version": (0, 0, 1),
    "license": "GPL",
    "location": "Sequencer",
    "warning": "",
    "category": "Sequencer",
}

from .operaciones.audio import insertaraudio, add_hotkey_audio, remove_hotkey_audio

from . import mipanel

classes = [
    insertaraudio,
    mipanel.mipanel
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    add_hotkey_audio()


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    remove_hotkey_audio()
