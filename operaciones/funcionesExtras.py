import bpy
import blf

def asignarDinámica(objeto, atributo, valor) -> bool:
    """Asigna de forma dinámica al valor

        en equivalente a 
        objeto.atributo = valor
    """
    atributos = atributo.split('.')

    for atributoTemporal in atributos[:-1]:
        if hasattr(objeto, atributoTemporal):
            objeto = getattr(objeto, atributoTemporal)
        else:
            print(f"El atributo '{atributoTemporal}' no existe.")
            return False

    last_attr = atributos[-1]
    if hasattr(objeto, last_attr):
        setattr(objeto, last_attr, valor)
        return True
    else:
        print(f"El atributo '{last_attr}' no existe en '{objeto}'.")
        return False


def obtenerObjetoAtributo(objeto, atributo):
    atributos = atributo.split('.')

    for atributoTemporal in atributos[:-1]:
        if hasattr(objeto, atributoTemporal):
            objeto = getattr(objeto, atributoTemporal)
        else:
            print(f"El atributo '{atributoTemporal}' no existe.")
            return

    return objeto


def trasformarFrame(tiempo, frame):

    h, m, s = tiempo.split(":")
    return int((int(h) * 3600 + int(m) * 60 + float(s)) * frame)

def cargarFuente(archivoFuente: str) -> tuple:
    """Carga una fuente en Blender, devuelve su ID Selection y ID Para calculo de tamaño de fuente
    Args:
        archivoFuente (str): Ruta del archivo de fuente a cargar.
    """
    fuenteCargada = False
    idFuenteSelection = 0
    
    for fuente in bpy.data.fonts:
            if archivoFuente in fuente.filepath: 
                fuenteCargada = True
                break
            idFuenteSelection += 1
            
    if not fuenteCargada:
        bpy.data.fonts.load(archivoFuente)
        bpy.ops.file.make_paths_relative()
    
    idFuente = blf.load(archivoFuente)
    return idFuenteSelection, idFuente
