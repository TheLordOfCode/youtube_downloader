import yt_dlp
import os
from pathlib import Path
from tkinter import Tk, Label, Button, Entry, filedialog, messagebox, StringVar, Text, Scrollbar, Frame
from tkinter import ttk
import threading


class DescargadorYouTube:
    def __init__(self, root):
        self.root = root
        self.root.title("Descargador de YouTube")
        self.root.geometry("650x500")
        self.root.resizable(False, False)
        
        self.output_dir = ""
        self.descargando = False
        
        # Configurar interfaz
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Título
        Label(self.root, text="📥 Descargador de Videos de YouTube", 
              font=("Arial", 16, "bold")).pack(pady=15)
        Label(self.root, text="Descarga videos en la mejor calidad disponible sin FFmpeg", 
              font=("Arial", 9)).pack(pady=5)
        
        # Frame para URL
        frame_url = Frame(self.root)
        frame_url.pack(pady=10, padx=20, fill="x")
        
        Label(frame_url, text="🔗 URL del video:", font=("Arial", 10, "bold")).pack(anchor="w")
        self.url_var = StringVar()
        self.entry_url = Entry(frame_url, textvariable=self.url_var, font=("Arial", 10), width=60)
        self.entry_url.pack(pady=5, fill="x")
        self.entry_url.focus()
        
        # Botón para seleccionar carpeta
        Button(self.root, text="📂 Seleccionar carpeta de descarga", 
               command=self.seleccionar_carpeta, width=35, height=2,
               bg="#2196F3", fg="white", font=("Arial", 10, "bold")).pack(pady=10)
        
        self.lbl_carpeta = Label(self.root, text="Carpeta: descargas (por defecto)", 
                                 font=("Arial", 9), fg="#666")
        self.lbl_carpeta.pack()
        
        # Botón de descarga
        self.btn_descargar = Button(self.root, text="⬇️ DESCARGAR VIDEO", 
                                     command=self.iniciar_descarga, width=30, height=2,
                                     bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
        self.btn_descargar.pack(pady=15)
        
        # Frame para consola de salida
        frame_consola = Frame(self.root)
        frame_consola.pack(pady=10, padx=20, fill="both", expand=True)
        
        Label(frame_consola, text="📋 Estado de la descarga:", 
              font=("Arial", 10, "bold")).pack(anchor="w")
        
        # Scrollbar y Text widget
        scrollbar = Scrollbar(frame_consola)
        scrollbar.pack(side="right", fill="y")
        
        self.text_consola = Text(frame_consola, height=10, width=70, 
                                 font=("Courier", 9), yscrollcommand=scrollbar.set,
                                 bg="#f5f5f5", fg="#333")
        self.text_consola.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.text_consola.yview)
        
        # Barra de progreso
        self.progress_var = StringVar(value="Esperando...")
        self.lbl_progreso = Label(self.root, textvariable=self.progress_var, 
                                  font=("Arial", 9), fg="#4CAF50")
        self.lbl_progreso.pack(pady=5)
    
    def seleccionar_carpeta(self):
        carpeta = filedialog.askdirectory(title="Seleccionar carpeta de descarga")
        if carpeta:
            self.output_dir = carpeta
            self.lbl_carpeta.config(text=f"Carpeta: {carpeta}")
            self.log(f"✓ Carpeta seleccionada: {carpeta}")
    
    def log(self, mensaje):
        """Añade mensaje a la consola"""
        self.text_consola.insert("end", mensaje + "\n")
        self.text_consola.see("end")
        self.root.update()
    
    def iniciar_descarga(self):
        url = self.url_var.get().strip()
        
        if not url:
            messagebox.showwarning("Advertencia", "Por favor ingresa una URL de YouTube")
            return
        
        if self.descargando:
            messagebox.showinfo("Info", "Ya hay una descarga en progreso")
            return
        
        # Limpiar consola
        self.text_consola.delete(1.0, "end")
        
        # Usar carpeta por defecto si no se seleccionó ninguna
        carpeta = self.output_dir if self.output_dir else "descargas"
        
        # Descargar en un hilo separado para no bloquear la interfaz
        self.descargando = True
        self.btn_descargar.config(state="disabled", bg="#cccccc")
        thread = threading.Thread(target=self.descargar_video, args=(url, carpeta))
        thread.daemon = True
        thread.start()
    
    def descargar_video(self, url, carpeta_destino):
        """Descarga el video de YouTube"""
        try:
            # Crear carpeta si no existe
            Path(carpeta_destino).mkdir(parents=True, exist_ok=True)
            
            self.log("="*60)
            self.log("🎥 DESCARGADOR DE YOUTUBE")
            self.log("="*60)
            self.log("")
            
            # Configuración de yt-dlp
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': os.path.join(carpeta_destino, '%(title)s.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
                'progress_hooks': [self.mostrar_progreso],
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Obtener información del video
                self.log("📋 Obteniendo información del video...")
                self.progress_var.set("Obteniendo información...")
                
                info = ydl.extract_info(url, download=False)
                titulo = info.get('title', 'Sin título')
                duracion = info.get('duration', 0)
                resolucion = info.get('resolution', 'Desconocida')
                
                self.log(f"✓ Título: {titulo}")
                self.log(f"✓ Duración: {duracion // 60}:{duracion % 60:02d} minutos")
                self.log(f"✓ Resolución: {resolucion}")
                self.log("")
                self.log("⬇️ Iniciando descarga...")
                self.log("")
                
                # Descargar el video
                ydl.download([url])
                
                self.log("")
                self.log("="*60)
                self.log("✅ ¡DESCARGA COMPLETADA EXITOSAMENTE!")
                self.log(f"📁 Guardado en: {os.path.abspath(carpeta_destino)}")
                self.log("="*60)
                
                self.progress_var.set("✅ Descarga completada")
                
                # Mostrar mensaje de éxito
                self.root.after(0, lambda: messagebox.showinfo(
                    "Descarga exitosa", 
                    f"✅ Video descargado correctamente\n\nTítulo: {titulo}\n\nUbicación:\n{os.path.abspath(carpeta_destino)}"
                ))
                
        except Exception as e:
            self.log("")
            self.log(f"❌ ERROR: {str(e)}")
            self.progress_var.set("❌ Error en la descarga")
            self.root.after(0, lambda: messagebox.showerror(
                "Error", 
                f"No se pudo descargar el video:\n\n{str(e)}"
            ))
        
        finally:
            self.descargando = False
            self.root.after(0, lambda: self.btn_descargar.config(state="normal", bg="#4CAF50"))
    
    def mostrar_progreso(self, d):
        """Callback para mostrar el progreso de descarga"""
        if d['status'] == 'downloading':
            porcentaje = d.get('_percent_str', '0%').strip()
            velocidad = d.get('_speed_str', 'N/A').strip()
            descargado = d.get('_downloaded_bytes_str', '0').strip()
            total = d.get('_total_bytes_str', '?').strip()
            
            mensaje = f"📥 {porcentaje} | {descargado}/{total} | {velocidad}"
            self.progress_var.set(mensaje)
            
        elif d['status'] == 'finished':
            self.log("✓ Descarga finalizada, procesando archivo...")
            self.progress_var.set("Procesando archivo...")


def main():
    root = Tk()
    app = DescargadorYouTube(root)
    root.mainloop()


if __name__ == "__main__":
    main()