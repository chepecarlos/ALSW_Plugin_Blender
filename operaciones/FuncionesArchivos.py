"""Libreria de Funciones para Lectura y escritura de archivos."""

import json
import os
import sys

from pathlib import Path


def ObtenerFolderConfig():
    """Devuelte ruta donde esta el folder de configuracion."""
    Folder = UnirPath(Path.home(), '.config/elgatoalsw-cli')

    return Folder


def ObtenerArchivo(Archivo):
    """Leer y devuelte la informacion de un archivo dentro del folde de configuraciones."""
    ArchivoConfig = ObtenerFolderConfig()
    if Archivo.endswith(".json"):
        ArchivoActual = UnirPath(ArchivoConfig, Archivo)
        if os.path.exists(ArchivoActual):
            with open(ArchivoActual) as f:
                return json.load(f)
    return None


def ObtenerValor(Archivo, Atributo, Depurar=True):
    """Obtiene un Atributo de un Archivo."""
    data = ObtenerArchivo(Archivo)

    if data is None:
        print(f"Archivo no Exite {Archivo}")
        return None

    Tipo = type(Atributo)
    if Tipo is list:
        if len(Atributo) >= 2:
            if Atributo[0] in data:
                if Atributo[1] in data[Atributo[0]]:
                    return data[Atributo[0]][Atributo[1]]
    else:
        if Atributo in data:
            return data[Atributo]

    if Depurar:
        print(f"No existe el atributo {Atributo}")
    return None


def SalvarArchivo(Archivo, Data):
    """Sobre escribe data en archivo."""
    ArchivoConfig = ObtenerFolderConfig()
    Archivo = UnirPath(ArchivoConfig, Archivo)
    with open(Archivo, 'w+') as f:
        json.dump(Data, f, indent=1)


def SalvarValor(Archivo, Atributo, Valor, local=True):
    """Salvar un Valor en Archivo."""
    data = dict()
    ArchivoConfig = ObtenerFolderConfig()
    if local:
        Archivo = UnirPath(ArchivoConfig, Archivo)
    
    data = ObtenerArchivo(Archivo)
    if data is None:
        return None
   
    Tipo = type(Atributo)
    if Tipo is list:
        # TODO Buscar como insertar para mas de nos niveles
        if len(Atributo) >= 2:
            if not Atributo[0] in data:
                data[Atributo[0]] = dict()
            data[Atributo[0]][Atributo[1]] = Valor
    else:
        data[Atributo] = Valor

    with open(Archivo, 'w') as f:
        json.dump(data, f, indent=2)


def UnirPath(Path1, Path2):
    """Une dos direciones."""
    return os.path.join(Path1, Path2)


def RelativoAbsoluto(Path, FolderActual):
    """Convierte Direcion relativas en absolutas."""
    if Path.startswith("./"):
        return UnirPath(FolderActual, QuitarPrefixInicio(Path, "./"))
    return Path


def QuitarPrefixInicio(text, prefix):
    """Quita un Prefijo o patron del inicio de una cadena."""
    return text[text.startswith(prefix) and len(prefix):]


def ObtenerListaFolder(Directorio):
    """Devuelve una lista de los folder dentro de Directorio."""
    ArchivoConfig = ObtenerFolderConfig()
    FolderActual = os.path.join(ArchivoConfig, Directorio)
    ListaFolder = []
    if os.path.exists(FolderActual):
        for folder in os.listdir(FolderActual):
            if os.path.isdir(os.path.join(FolderActual, folder)):
                # ListaFolder.append({"folder": folder})
                ListaFolder.append(folder)
        return ListaFolder
    return None


def ObtenerListaArhivos(Directorio):
    """Obtiene una lista de Archivo en un directorio."""
    ArchivoConfig = ObtenerFolderConfig()
    FolderActual = UnirPath(ArchivoConfig, Directorio)
    ListaArchivos = []
    if os.path.exists(FolderActual):
        for archivo in os.listdir(FolderActual):
            if os.path.isfile(UnirPath(FolderActual, archivo)):
                ListaArchivos.append(archivo)
        return ListaArchivos
    return None
