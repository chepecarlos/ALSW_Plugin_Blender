


def asignarDinámica(objeto, atributo, valor):
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
            return 

    last_attr = atributos[-1]
    if hasattr(objeto, last_attr):
        setattr(objeto, last_attr, valor)
    else:
        print(f"El atributo '{last_attr}' no existe en '{objeto}'.")
        
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