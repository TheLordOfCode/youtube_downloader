# 📥 Descargador de Videos de YouTube (GUI)

Aplicación gráfica escrita en **Python** que permite descargar videos de **YouTube** en la mejor calidad disponible, utilizando la librería `yt-dlp`.  
No requiere FFmpeg ni configuraciones avanzadas. Ideal para uso personal y educativo.

---

## 🚀 Características

- Interfaz gráfica desarrollada con **Tkinter**.  
- Descarga videos de YouTube en formato **.mp4** con la mejor calidad disponible.  
- Permite seleccionar la carpeta de destino.  
- Muestra en tiempo real el progreso y el estado de la descarga.  
- No bloquea la interfaz durante la descarga (usa hilos).  
- Compatible con **Windows**, **Linux** y **macOS**.

---

## 🧰 Requisitos

- Python **3.8** o superior  
- Conexión a Internet  
- Dependencias listadas en `requirements.txt`

---

## ⚙️ Instalación

1. Clona este repositorio o descarga el archivo `youtube_downloader.py`:

```bash
git clone https://github.com/tu_usuario/youtube_downloader.git
cd youtube_downloader
```

2. Instala las dependencias necesarias:

```bash
pip install -r requirements.txt
```

3. Ejecuta el programa:

```bash
python youtube_downloader.py
```

---

## 📂 Estructura del proyecto

```
youtube_downloader/
│
├── youtube_downloader.py    # Código principal
├── requirements.txt         # Dependencias necesarias
└── README.md                # Documentación
```

---

## 📦 Dependencias principales

- **yt-dlp** → Descarga y manejo de videos de YouTube.
- **tkinter** → Interfaz gráfica (incluida por defecto en Python).

---

## 💡 Notas

- Si no seleccionas una carpeta, los videos se guardarán automáticamente en una carpeta llamada `descargas` en el mismo directorio del script.  
- Si `yt-dlp` detecta restricciones en un video, puede requerir actualización del paquete mediante:

```bash
pip install -U yt-dlp
```

---

## 👨‍💻 Autor

**Juan Quevedo**  
Proyecto educativo en Python — 2025

---

## 🪪 Licencia

Este proyecto se distribuye bajo la licencia **MIT**, por lo que puedes modificarlo y usarlo libremente con atribución.
