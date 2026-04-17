Este reproductor de audio es una aplicación para desktop desarrollada en Python. Utiliza una interfaz gráfica basada en tkinter y el motor de audio pygame para ofrecer una experiencia de reproducción de música eficiente, con soporte para metadatos y gestión de listas de reproducción personalizadas.

## Características

* **Compatibilidad Multiformato:** Soporta una amplia gama de extensiones, incluyendo .mp3, .wav, .ogg, .flac, y formatos MIDI.
* **Gestión de Metadatos:** Extracción automática de títulos, artistas, álbumes y géneros mediante la librería tinytag.
* **Visualización de Portadas:** Capacidad para renderizar el arte de tapa embebido en los archivos de audio (a falta de este se muestra un cover predeterminado.
* **Sistema de Búsqueda:** Motor de búsqueda interno para localizar canciones específicas dentro de la biblioteca cargada.
* **Gestión de Playlists:** Funcionalidad para crear playlists personalizadas mediante la copia y organización de archivos en directorios locales.
* **Persistencia de Datos:** Utiliza el formato JSONL para el almacenamiento y la lectura de la base de datos de canciones.

##  Requisitos 

Para ejecutar esta aplicación, es necesario contar con Python 3.x y las siguientes dependencias:

* `tkinter`: Para la interfaz gráfica. Suele estar preinstalado a diferencia del resto.
* `pygame`: Para el procesamiento y salida de audio.
* `tinytag`: Para la lectura de metadatos.
* `Pillow` (PIL): Para mostrar imágenes.


Puedes instalarlas ejecutando:
```bash o cmd
pip install tkinter pygame tinytag Pillow
```
---

This audio player is a desktop application developed in Python. It utilizes a tkinter-based UI and the pygame audio engine to deliver an efficient music playback experience, featuring metadata support and custom playlist management.

## Features

* **Multi-format Compatibility:** Supports a wide range of extensions, including .mp3, .wav, .ogg, .flac, and MIDI formats.
* **Metadata Management:** Automatic extraction of titles, artists, albums, and genres using the tinytag library.
* **Cover Art Visualization:** Capability to render embedded cover art from audio files (if missing, a default cover is displayed).
* **Search System:** Internal search engine to locate specific songs within the loaded library.
* **Playlist Management:** Functionality to create custom playlists by organizing and copying files into local directories.
* **Data Persistence:** Uses the JSONL format for storage and reading of the song database.

## Requirements 

To run this application, Python 3.x and the following dependencies are required:
* `tkinter`: For the UI (it's usually pre-installed)
* `pygame`: For audio processing and output.
* `tinytag`: For reading metadata.
* `Pillow` (PIL): For displaying images.

You can install them by running:
```bash or cmd
pip install tkinter pygame tinytag Pillow

