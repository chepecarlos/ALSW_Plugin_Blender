import bpy
from . import mipanel
from .operaciones.alinear import superaliniar
from .operaciones.audio import insertaraudio
from .operaciones.zoon import superzoon
from .operaciones.clip import insertarsonido
from .operaciones.insertarimagen import insertarimagen
from .operaciones.mover import moverclip
from .operaciones.indice import superindice
from .operaciones.exportar import exportarindice
from .operaciones.macros import add_hotkey, remove_hotkey

bl_info = {
    "name": "ALSW_Plugin_Blender",
    "author": "ChepeCarlos",
    "description": "Heramientas Extra para Sequencer",
    "blender": (2, 92, 0),
    "version": (0, 0, 5),
    "license": "GPL",
    "location": "Sequencer",
    "warning": "",
    "category": "Sequencer",
}

classes = [
    insertaraudio,
    insertarimagen,
    superaliniar,
    superzoon,
    insertarsonido,
    moverclip,
    superindice,
    exportarindice,
    mipanel.mi_PT_panel
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    add_hotkey()


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    remove_hotkey()
