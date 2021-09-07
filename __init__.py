import bpy
from . import mipanel
from .operaciones.alinear import superaliniar
from .operaciones.audio import insertaraudio
from .operaciones.zoon import superzoon
from .operaciones.clip import insertarsonido
from .operaciones.mover import moverclip
from .operaciones.indice import superindice
from .operaciones.exportar import exportarindice
from .operaciones.macros import add_hotkey, remove_hotkey

bl_info = {
    "name": "ALSW_Plugin_Blender",
    "author": "ChepeCarlos",
    "description": "Heramientas Extra para Sequencer",
    "blender": (2, 93, 3),
    "version": (0, 0, 3),
    "license": "GPL",
    "location": "Sequencer",
    "warning": "",
    "category": "Sequencer",
}

classes = [
    insertaraudio,
    superaliniar,
    superzoon,
    insertarsonido,
    moverclip,
    superindice,
    exportarindice,
    mipanel.mipanel
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    add_hotkey()


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    remove_hotkey()
