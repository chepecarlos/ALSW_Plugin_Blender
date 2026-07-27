# ChepeCarlos Plugin for Blender

Un plugin completo para Blender 5.x que acelera el flujo de trabajo en el Sequence Editor con herramientas potentes de edición de video y audio.

## 📋 Tabla de Contenidos

- [Instalación](#instalación)
- [Comandos de Desarrollo (Makefile)](#comandos-de-desarrollo-makefile)
- [Funciones Principales](#funciones-principales)
- [Cómo Usar](#cómo-usar)
- [Configuración](#configuración)
- [Atajos de Teclado](#atajos-de-teclado)

## 📦 Instalación

1. **Descargar el plugin:**
   - Clona o descarga este repositorio en tu máquina

2. **Instalar en Blender:**
   - Abre Blender 5.1.0 o superior
   - Ve a `Edit` → `Preferences` → `Add-ons`
   - Haz clic en `Install` y selecciona la carpeta del plugin
   - Busca "ChepeCarlos_Plugin_Blender" y actívalo

3. **Verificar instalación:**
   - Abre el Sequence Editor
   - En el panel lateral derecho (presiona `N`), verás una pestaña llamada "ChepeCarlos"

## 🛠️ Comandos de Desarrollo (Makefile)

El `Makefile` incluye recetas para desarrollar, probar e instalar el addon sin necesidad de abrir la UI de Blender manualmente. Usa **Flatpak** por defecto (`flatpak run org.blender.Blender`).

### Variables principales

| Variable | Valor por defecto | Descripción |
|---|---|---|
| `BLENDER` | `flatpak run org.blender.Blender` | Comando para lanzar Blender |
| `PROJECT_ROOT` | `/home/chepecarlos/5.Programas/1.Edicion` | Carpeta padre del addon para que Python lo encuentre |
| `ADDON_MODULE` | `ChepeCarlos_Plugin_Blender` | Nombre del módulo Python del addon |
| `DIST_DIR` | `dist` | Carpeta donde se guardan los ZIPs generados |
| `BLENDER_CONFIG_VERSION` | `5.1` | Versión de Blender para construir la ruta de addons |
| `ADDONS_DIR` | `~/.var/app/org.blender.Blender/config/blender/5.1/scripts/addons` | Carpeta donde Blender busca addons instalados (Flatpak) |

Puedes sobreescribir cualquier variable al vuelo sin editar el archivo:

```bash
make install-local BLENDER=/ruta/a/otro/blender
```

### Recetas disponibles

#### `make blenderaddon-bg` ⭐ (más usada en desarrollo)

```bash
make blenderaddon-bg
```

Lanza Blender en **modo background** (sin abrir ventana), importa el addon, lo registra e imprime `REGISTER_OK`, luego lo desregistra e imprime `UNREGISTER_OK`. Es la forma más rápida de verificar que el addon no tiene errores de sintaxis o registro.

---

#### `make blenderaddon-check`

```bash
make blenderaddon-check
```

Lanza Blender en background e imprime la versión instalada (`bpy.app.version_string`). Útil para confirmar qué versión está usando el Flatpak.

---

#### `make blenderaddon-dev`

```bash
make blenderaddon-dev
```

Lanza Blender **con tu configuración personal** (sin `--factory-startup`) y hace un `importlib.reload` del addon antes de registrarlo. Úsalo durante el desarrollo para probar cambios con tu entorno habitual.

---

#### `make blenderaddon`

```bash
make blenderaddon
```

Lanza Blender con `--factory-startup` (ignora tu configuración personal) e importa y registra el addon. Prueba rápida de carga, pero abre la UI completa.

---

#### `make blenderaddon-reload`

```bash
make blenderaddon-reload
```

Ciclo completo de prueba: registra el addon, limpia todos sus módulos de `sys.modules`, reimporta, hace `reload`, desregistra y vuelve a registrar. Verifica que el addon sobrevive un reload sin dejar estado sucio.

---

#### `make install-local`

```bash
make install-local
```

Copia el addon directamente a `ADDONS_DIR` usando `rsync` (excluye `.git`, `__pycache__`, `.vscode` y `dist/`). Después de esto puedes activar el addon desde Preferencias de Blender sin instalar un ZIP manualmente.

---

#### `make zip`

```bash
make zip
```

Empaca el addon como un ZIP instalable en `dist/`. El nombre incluye un timestamp (`ChepeCarlos_Plugin_Blender-YYYYMMDD-HHMMSS.zip`), listo para instalar desde la UI de Blender.

---

#### `make zlip`

Alias de `make zip`. Existe para no perder tiempo si uno escribe mal el comando.

---

## 🎬 Funciones Principales

### 1. **Insertar Clip**
Inserta imágenes, videos o archivos de audio en la posición del cursor actual del timeline.

**Ubicación:** Panel ChepeCarlos → `Insertar`

**Archivo de configuración:** `~/.config/pluginBlenderChepeCarlos/data/insertar.json`

**Parámetros configurables:**
| Parámetro  | Tipo   | Predeterminado | Descripción                             |
| ---------- | ------ | -------------- | --------------------------------------- |
| clip       | string | -              | Ruta absoluta del archivo a insertar    |
| volumen    | float  | 1              | Nivel de volumen (solo para audio)      |
| desface    | float  | 0              | Desplazamiento en frames                |
| duracion   | float  | 60             | Duración en frames                      |
| posicion_x | int    | 0              | Posición en eje X (para imágenes/video) |
| posicion_y | int    | 0              | Posición en eje Y (para imágenes/video) |
| origen_x   | float  | 0.5            | Origen X para transformaciones          |
| origen_y   | float  | 0.5            | Origen Y para transformaciones          |
| opacidad   | float  | 1              | Nivel de opacidad (0-1)                 |
| escala     | float  | 1              | Factor de escala                        |
| angulo     | float  | 0              | Ángulo de rotación en grados            |

**Ejemplo de uso:**
```json
{
  "clip": "/home/usuario/videos/intro.mp4",
  "volumen": 1.0,
  "desface": 0,
  "duracion": 120,
  "posicion_x": 0,
  "posicion_y": 0,
  "origen_x": 0.5,
  "origen_y": 0.5,
  "opacidad": 1.0,
  "escala": 1.0,
  "angulo": 0
}
```

### 2. **Sobreponer Audio**
Coloca automáticamente un clip de audio sobre uno o más clips seleccionados en el timeline.

**Ubicación:** Panel ChepeCarlos

**Uso:**
- Selecciona uno o más clips en el timeline
- Haz clic en "Sobreponer Audio"
- El audio se posicionará encima de los clips seleccionados con volumen automático

### 3. **Música sobre Clip**
Añade una pista de música sobre clips seleccionados con configuración automática de volumen y visualización de forma de onda.

**Ubicación:** Panel ChepeCarlos → `MrTee`

**Características:**
- Posiciona automáticamente el audio
- Muestra la forma de onda
- Ajusta volumen a 0.3 por defecto

### 4. **Alinear Clips**
Alinea automáticamente múltiples clips seleccionados en el timeline.

**Ubicación:** Panel ChepeCarlos → `Ariba`

**Uso:**
- Selecciona 2 o más clips
- Presiona el botón de Alinear
- Los clips se alinearán horizontalmente

### 5. **Zoom/Escala de Clips**
Amplía o reduce el tamaño de clips seleccionados.

**Ubicación:** Panel ChepeCarlos

**Uso:**
- Selecciona uno o más clips de video/imagen
- Ajusta los parámetros de escala
- La transformación se aplica automáticamente

### 6. **Mover Clip**
Desplaza clips seleccionados en direcciones específicas.

**Funciones:**
- Mover a la derecha en el timeline
- Mover a la izquierda en el timeline
- Mover hacia arriba (diferentes canales)
- Mover hacia abajo (diferentes canales)

### 7. **Generador de Índices (Marcadores como Texto)**
Convierte marcadores del timeline en clips de texto superpuestos en el video.

**Ubicación:** Panel ChepeCarlos → `Agregar`

**Uso:**
1. Crea marcadores en el timeline (presiona `M`)
2. Asigna nombres a los marcadores
3. Ejecuta "Generador de Índices"
4. Los marcadores se convertirán en clips de texto

### 8. **Copiar Tiempo del Cursor (Hueva)**
Copia el tiempo actual del cursor al portapapeles para referencia rápida.

**Ubicación:** Panel ChepeCarlos → `Hueva`

**Uso:** Muy útil para documentar tiempos específicos durante la edición

### 9. **Exportar Índices Extras**
Exporta información de marcadores extras para procesamiento posterior o documentación.

**Ubicación:** Panel ChepeCarlos

**Nota:** Solo funciona si hay marcadores con prefijos especiales en la escena

**Tipos de prefijos para marcadores:**
| Prefijo | Tipo           | Ejemplo                |
| ------- | -------------- | ---------------------- |
| >T      | Tarjeta/Title  | >T Créditos            |
| >L      | Link           | >L www.ejemplo.com     |
| >V      | Video          | >V Tutorial Completo   |
| >A      | Ads/Publicidad | >A Publicidad Sponsors |
| >C      | Créditos       | >C Música por: Artista |
| >P      | Pantalla Final | >P Suscribete ahora    |
| >E      | Recursos       | >E Imágenes: Unsplash  |

### 10. **Subtítulos**
Gestiona y procesa archivos de subtítulos sincronizados con el video.

**Ubicación:** Panel ChepeCarlos

**Archivo de configuración:** `~/.config/pluginBlenderChepeCarlos/data/blender_subtitulo.json`

**Características:**
- Carga automática de archivos .srt
- Sincronización con timeline
- Visualización automática

### 11. **Auto Anotar**
Anotaciones automáticas en clips para documentación rápida.

**Ubicación:** Panel ChepeCarlos

**Uso:**
- Selecciona clips
- Haz clic en Auto Anotar
- Las notas se guardan en metadatos

### 12. **Animar Clip**
Aplica animaciones predefinidas a clips seleccionados.

**Ubicación:** Panel ChepeCarlos

**Tipos de animaciones disponibles:**
- Zoom in/out gradual
- Movimiento/Pan
- Fade in/out
- Rotación suave
- Cambio de opacidad

### 13. **Palabras Por Minuto (PPM)**
Calcula las palabras por minuto de un script o narración para verificar tiempos de locución.

**Ubicación:** Panel ChepeCarlos → `Calcular`

**Uso:**
1. Selecciona el clip de audio o carga un archivo de script
2. Haz clic en "Calcular PPM"
3. El resultado se muestra en la consola de Blender
4. Útil para sincronizar narración con tiempo disponible

## 🎮 Cómo Usar

### Acceder al Panel del Plugin

1. Abre el **Sequence Editor** en Blender
   - Puedes abrirlo desde `Editor Type` en cualquier editor
   - O acceder desde la ventana superior: `Editor` → `Sequence Editor`

2. Presiona `N` para abrir el panel lateral (si está cerrado)

3. Busca la pestaña **"ChepeCarlos"** en el panel lateral derecho

### Flujo de trabajo típico

#### Insertar Clips
1. Coloca el cursor en el timeline donde quieres insertar el clip
2. Configura el archivo en `~/.config/pluginBlenderChepeCarlos/data/insertar.json` con la ruta absoluta del archivo
3. Haz clic en "Insertar"
4. El clip se agregará en la posición del cursor

#### Editar Clips
1. Selecciona clips con `LMB` (clic izquierdo)
2. Usa las herramientas disponibles:
   - **Alinear**: Para sincronizar múltiples clips
   - **Mover**: Para desplazar en el timeline
   - **Escala/Zoom**: Para redimensionar
3. Ajusta propiedades según sea necesario

#### Agregar Audio
1. Selecciona los clips donde quieres agregar audio
2. Usa "Sobreponer Audio" o "Música sobre Clip"
3. El audio se posicionará automáticamente

#### Agregar Marcadores como Texto
1. Crea marcadores en el timeline (presiona `M`)
2. Nombre los marcadores (servirán como texto)
3. Usa "Generador de Índices"
4. Los marcadores se convertirán en clips de texto

#### Exportar Marcos de Referencia
1. Crea marcadores con prefijos (>T, >L, >V, etc.)
2. Usa "Exportar Índices Extras"
3. Se generará un archivo de referencia para post-producción

## ⚙️ Configuración

### Archivos de Configuración

Los archivos de configuración se guardan en:

- `~/.config/pluginBlenderChepeCarlos/`

Ruta base real usada por el plugin:

- `~/.config/pluginBlenderChepeCarlos` (sin doble `.config`)

**Archivos principales (dentro de `~/.config/pluginBlenderChepeCarlos/`):**
- **`data/insertar.json`** - Configuración para insertar clips
- **`data/blender_subtitulo.json`** - Configuración de subtítulos
- **`data/blender_subtitulo_resaltado.json`** - Estilo de resaltado de palabras
- **`data/blender_subtitulo_extra.json`** - Ajustes extra de subtítulos (fuente, espera, etc.)
- **`data/blender.json`** - Configuración general del plugin

### Estructura de Directorios

```
ChepeCarlos_Plugin_Blender/
├── __init__.py                 # Inicializador del plugin
├── mipanel.py                  # Panel UI
├── README.md                   # Este archivo
├── Makefile                    # Compilación y pruebas
├── data/                       # Archivos de configuración
│   ├── insertar.json
│   ├── blender_subtitulo.json
│   └── blender.json
└── operaciones/                # Módulos de funcionalidades
    ├── alinear.py
    ├── exportar.py
    ├── exportarextras.py
    ├── hueva.py
    ├── indice.py
    ├── macros.py
    ├── mover.py
    ├── sobreponeraudio.py
    ├── subtitulos.py
    ├── superAnimar.py
    ├── superInsertar.py
    ├── zoon.py
    ├── autoanotar.py
    ├── palabraPorMinuto.py
    ├── extras.py
    ├── FuncionesArchivos.py
    └── funcionesExtras.py
```

### Valores por Defecto

**Para Insertar Clips:**
```json
{
  "clip": "/ruta/absoluta/archivo",
  "volumen": 1.0,
  "desface": 0,
  "duracion": 60,
  "posicion_x": 0,
  "posicion_y": 0,
  "origen_x": 0.5,
  "origen_y": 0.5,
  "opacidad": 1.0,
  "escala": 1.0,
  "angulo": 0
}
```

## ⌨️ Atajos de Teclado

El plugin soporta macros personalizadas. Los atajos se pueden definir en la configuración de macros de Blender.

**Atajos sugeridos (configurable):**
- `Ctrl + Shift + Y` - Insertar Clip (predeterminado)
- Otros atajos se pueden asignar según preferencia

Para asignar atajos personalizados:
1. Ve a `Edit` → `Preferences` → `Keymap`
2. Busca las operaciones del plugin (comienzan con `scene.`)
3. Asigna los atajos deseados

## 🐛 Solución de Problemas

### El plugin no aparece en Add-ons
**Solución:**
- Verifica que Blender sea versión 5.1.0 o superior
- Asegúrate de que activaste el plugin en las preferencias
- Reinicia Blender si es necesario

### Las funciones no funcionan o dan errores
**Solución:**
- Verifica que el Sequence Editor esté abierto
- Selecciona al menos un clip en el timeline (para funciones que lo requieran)
- Consulta la consola de Blender (`Window` → `Toggle System Console`)
- Revisa que los archivos de configuración JSON sean válidos

### Errores al insertar clips
**Solución:**
- Verifica que la ruta del archivo sea **absoluta** (no relativa)
- Asegúrate de que el archivo existe y es accesible
- Comprueba que tienes permisos de lectura en la carpeta
- Verifica que el archivo sea un formato soportado (MP4, PNG, WAV, etc.)

### El botón "Insertar" está deshabilitado
**Causa:** No hay un archivo configurado en `~/.config/pluginBlenderChepeCarlos/data/insertar.json`

**Solución:**
1. Crea el archivo `~/.config/pluginBlenderChepeCarlos/data/insertar.json`
2. Agrega la configuración con la ruta del archivo
3. Recarga el plugin

### Audio no sincronizado
**Solución:**
- Verifica que los clips tengan el same framerate
- Asegúrate de que el cursor está en la posición correcta del timeline
- Revisa que los clips no estén bloqueados

## 📋 Requisitos del Sistema

- **Blender:** 5.1.0 o superior
- **Python:** 3.11 o superior (incluido en Blender)
- **Sistema Operativo:** Windows, macOS o Linux
- **Espacio en disco:** ~50 MB

## ⚡ Performance

Este plugin está optimizado para trabajar de manera eficiente incluso con proyectos grandes:

- Rendering rápido de transformaciones
- Procesamiento por lotes para múltiples clips
- Caché automática para operaciones frecuentes

## 📚 Recursos Adicionales

- [Documentación de Blender Python API](https://docs.blender.org/api/current/)
- [Tutorial del Sequence Editor](https://docs.blender.org/manual/en/latest/editors/sequence/)
- [Guía de Scripting de Blender](https://docs.blender.org/manual/en/latest/advanced/scripting/)

## 📄 Licencia

GPL - Código libre y abierto

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para reportar bugs o sugerir mejoras:

1. Describe el problema o idea claramente
2. Incluye pasos para reproducir el error
3. Especifica tu versión de Blender y SO

## 👤 Autor

**ChepeCarlos** - Herramientas profesionales para edición de video en Blender

---

**Última actualización:** 17 de abril de 2026
**Versión del Plugin:** 0.2.0
**Versión mínima de Blender:** 5.1.0
