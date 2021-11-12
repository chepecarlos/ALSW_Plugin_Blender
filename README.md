# ALSW_Plugin_Blender

Plubin para ser mas feliz editando con atajos o macros que te ayudara a editar mas rapido

## Configurar

Los Atributos se guarda dentro de folder (~/.config/elgatoalsw-cli) para conbinar con proyecto [ElGatoALSW](https://github.com/chepecarlos/ElGatoALSW) de Macros, el archivo donde se guardan los atribuos es (data/blender.json)

## Macros

Macros en el sistema

## Insertar Clip

Inserta clip en posicion de Cursor, ya sea Audio, Video o Imagen

La ruta tiene que ser Absoluta

| Nombre   | Atributo | Tipo       | Defaul    | Ejemplo         |
| -------- | -------- | ---------- | --------- | --------------- |
| Direcion | clip     | stl        | Requerido | /home/pollo.png |
| Volumen  | volumen  | float (R+) | 1         | 1.2             |
| Desface  | desface  | float      | 0         | -10             |
| Duracion | duracion | float      | 60        | 10              |

Atajo de Teclado:

```
ctrl + shift + y
```

## Sobreponer Audio

Has clip sobre un o mas clip para agregar

## Exportar Extra

Exportar markas extras para ayudar en la preparacion de video

**Nota**: Solo funciona si existe Marcas

**Tipos de Prefijos**

| Nombre              | Prefijo | Ejemplo                      |
| ------------------- | ------- | ---------------------------- |
| Tarjeta             | >T      | >T Video de MQTT             |
| Link                | >L      | >L www.google.com            |
| Video               | >V      | >V Video MQTT                |
| Ads                 | >A      | >A Publicidad de Chepecarlos |
| Creditor            | >C      | >C Gracias por la musica a   |
| Pantalla Final      | >P      | >P Video de MQTT             |
| Recursos de Edición | >E      | >E Imágenes de arduino       |
