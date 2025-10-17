# Retro Player — Music Player

Un reproductor musical moderno con estética retro hecho en **Python + Tkinter**, que reproduce canciones en una interfaz visual con **animación de video de fondo**, barra de progreso y control de playlist.

<img width="1920" height="1020" alt="Captura de pantalla 2025-10-17 031642" src="https://github.com/user-attachments/assets/d329a69b-a039-4647-a06d-5cd694cefe16" />


---

## Características

Interfaz gráfica con estilo **neón retro**.  
Reproduce archivos **MP3, WAV y OGG**.  
Soporte para **playlist** con múltiples canciones.  
Controles completos:
- ▶ **Play**
- ⏸ **Pausa**
- ⏹ **Stop**
- ⏮ **Anterior**
- ⏭ **Siguiente**
- 🔁 **Loop ON/OFF**
- 🗑 **Limpiar playlist**

Muestra el **tiempo transcurrido y duración total**.  
Fondo animado con **video reproducido en bucle (OpenCV + Pillow)**.  
Diseño **responsivo**: los botones cambian de tamaño según la ventana.  
Interfaz visual hecha 100% con **Tkinter + ttk + Pygame Mixer**.

---

## 🧠 Tecnologías utilizadas

- [Python 3.x](https://www.python.org/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html)
- [pygame](https://www.pygame.org/docs/ref/mixer.html)
- [OpenCV](https://opencv.org/)
- [Pillow (PIL)](https://pillow.readthedocs.io/en/stable/)
- [threading](https://docs.python.org/3/library/threading.html)
- [time](https://docs.python.org/3/library/time.html)

---

## 🖥️ Requisitos previos

Antes de ejecutar el proyecto, asegúrate de tener instaladas las dependencias necesarias:

```bash
pip install pygame opencv-python Pillow
