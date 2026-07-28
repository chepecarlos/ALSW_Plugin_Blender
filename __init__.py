import bpy

from . import mipanel
from .operaciones.alinear import superaliniar
from .operaciones.exportar import exportarindice
from .operaciones.exportarextras import exportarextra
from .operaciones.hueva import hueva
from .operaciones.indice import superindice
from .operaciones.macros import add_hotkey, remove_hotkey
from .operaciones.mover import moverclip
from .operaciones.sobreponeraudio import sobreponeraudio
from .operaciones.subtitulos import subtitulo
from .operaciones.superInsertar import superInsertar
from .operaciones.zoon import superzoon
from .operaciones.autoanotar import autoanotar
from .operaciones.superAnimar import superanimar
from .operaciones.palabraPorMinuto import palabraPorMinuto
from .operaciones.preEditar import preEditar

bl_info = {
    "name": "ChepeCarlos_Plugin_Blender",
    "author": "ChepeCarlos",
    "description": "Herramientas Extra para Sequencer",
    "blender": (5, 1, 0),
    "version": (0, 2, 1),
    "license": "GPL",
    "location": "Sequencer",
    "warning": "",
    "support": "COMMUNITY",
    "category": "Sequencer",
}

classes = [
    sobreponeraudio,
    superInsertar,
    superaliniar,
    superzoon,
    moverclip,
    superindice,
    exportarextra,
    exportarindice,
    hueva,
    subtitulo,
    autoanotar,
    superanimar,
    palabraPorMinuto,
    preEditar,
    mipanel.mi_PT_panel,
]


def register():
    for cls in classes:
        # ponytail: register_class falla si ya hay una clase con el mismo
        # nombre registrada (p.ej. addon instalado + `make blenderaddon-dev`
        # a la vez). Por el cacheo de submódulos en sys.modules, `cls` puede
        # ser el MISMO objeto ya registrado, o uno distinto con igual nombre;
        # se desregistran ambos casos (ignorando si no estaban registrados).
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            pass
        for sub in cls.__bases__[0].__subclasses__():
            if sub is not cls and sub.__name__ == cls.__name__:
                try:
                    bpy.utils.unregister_class(sub)
                except RuntimeError:
                    pass
        bpy.utils.register_class(cls)
    add_hotkey()


def unregister():
    remove_hotkey()
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
