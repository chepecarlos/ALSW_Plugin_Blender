# ALSW_Plugin_Blender

Plubin para ser mas feliz editando con atajos o macros que te ayudara a editar mas rapido

## Configurar

Los Atributos se guarda dentro de folder (~/.config/elgatoalsw-cli) para conbinar con proyecto [ElGatoALSW](https://github.com/chepecarlos/ElGatoALSW) de Macros, el archivo donde se guardan los atribuos es (data/blender.json)

## Macros

Macros en el sistema

## Insertar Clip

Inserta clip en posicion de Cursor, ya sea Audio, Video o Imagen

La ruta tiene que ser Absoluta

| Nombre     | Atributo   | Tipo       | Requerido | Defaul    | Ejemplo         |
| ---------- | ---------- | ---------- | --------- | --------- | --------------- |
| Direction  | clip       | stl        | true      | Requerido | /home/pollo.png |
| Volumen    | volumen    | float (R+) | false     | 1         | 1.2             |
| Desfacé    | desface    | float      | false     | 0         | -10             |
| Duración   | duracion   | float      | false     | 60        | 10              |
| Posición X | posicion_x | int        | false     | 0         | 300             |
| Posición y | posicion_y | int        | false     | 0         | 22              |
| Origen X   | origen_x   | float      | false     | 0.5       | 0,3             |
| Origen Y   | origen_y   | float      | false     | 0.5       | 0,3             |
| Opacidad   | opacidad   | float      | false     | 1         | 0.2             |
| Escala     | escala     | float      | false     |           | 3               |

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
