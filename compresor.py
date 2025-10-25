import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import os

class ImageCompressor(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana
        self.title("Compresor de Imágenes")
        self.geometry("600x500")
        
        # Tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Variables
        self.image_path = None
        self.original_size = 0
        
        # Título
        self.title_label = ctk.CTkLabel(
            self, 
            text="🖼️ Compresor de Imágenes",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=20)
        
        # Frame para selección de archivo
        self.file_frame = ctk.CTkFrame(self)
        self.file_frame.pack(pady=10, padx=20, fill="x")
        
        self.select_button = ctk.CTkButton(
            self.file_frame,
            text="Seleccionar Imagen",
            command=self.select_image,
            width=200,
            height=40
        )
        self.select_button.pack(pady=15)
        
        self.file_label = ctk.CTkLabel(
            self.file_frame,
            text="No se ha seleccionado ninguna imagen",
            wraplength=500
        )
        self.file_label.pack(pady=5)
        
        # Frame para información
        self.info_frame = ctk.CTkFrame(self)
        self.info_frame.pack(pady=10, padx=20, fill="x")
        
        self.size_label = ctk.CTkLabel(
            self.info_frame,
            text="Tamaño original: --",
            font=ctk.CTkFont(size=12)
        )
        self.size_label.pack(pady=5)
        
        self.dimensions_label = ctk.CTkLabel(
            self.info_frame,
            text="Dimensiones: --",
            font=ctk.CTkFont(size=12)
        )
        self.dimensions_label.pack(pady=5)
        
        # Frame para controles de compresión
        self.compression_frame = ctk.CTkFrame(self)
        self.compression_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.quality_label = ctk.CTkLabel(
            self.compression_frame,
            text="Calidad de compresión: 85%",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.quality_label.pack(pady=10)
        
        self.quality_slider = ctk.CTkSlider(
            self.compression_frame,
            from_=1,
            to=100,
            number_of_steps=99,
            command=self.update_quality_label,
            width=400
        )
        self.quality_slider.set(85)
        self.quality_slider.pack(pady=10)
        
        self.quality_info = ctk.CTkLabel(
            self.compression_frame,
            text="Mayor calidad = Mayor tamaño de archivo\nMenor calidad = Menor tamaño de archivo",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        self.quality_info.pack(pady=5)
        
        # Frame para formato de salida
        self.format_label = ctk.CTkLabel(
            self.compression_frame,
            text="Formato de salida:",
            font=ctk.CTkFont(size=12)
        )
        self.format_label.pack(pady=(15, 5))
        
        self.format_var = ctk.StringVar(value="JPEG")
        self.format_menu = ctk.CTkOptionMenu(
            self.compression_frame,
            values=["JPEG", "PNG", "WebP"],
            variable=self.format_var,
            width=200
        )
        self.format_menu.pack(pady=5)
        
        # Botón de comprimir
        self.compress_button = ctk.CTkButton(
            self,
            text="Comprimir y Guardar",
            command=self.compress_image,
            width=250,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            state="disabled"
        )
        self.compress_button.pack(pady=20)
        
    def select_image(self):
        file_path = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[
                ("Imágenes", "*.jpg *.jpeg *.png *.bmp *.gif *.webp"),
                ("Todos los archivos", "*.*")
            ]
        )
        
        if file_path:
            self.image_path = file_path
            filename = os.path.basename(file_path)
            self.file_label.configure(text=f"Archivo: {filename}")
            
            # Obtener información de la imagen
            self.original_size = os.path.getsize(file_path)
            size_mb = self.original_size / (1024 * 1024)
            self.size_label.configure(text=f"Tamaño original: {size_mb:.2f} MB")
            
            with Image.open(file_path) as img:
                width, height = img.size
                self.dimensions_label.configure(
                    text=f"Dimensiones: {width} x {height} px"
                )
            
            self.compress_button.configure(state="normal")
    
    def update_quality_label(self, value):
        self.quality_label.configure(text=f"Calidad de compresión: {int(value)}%")
    
    def compress_image(self):
        if not self.image_path:
            messagebox.showerror("Error", "Por favor selecciona una imagen primero")
            return
        
        # Pedir ubicación para guardar
        format_ext = self.format_var.get().lower()
        if format_ext == "jpeg":
            format_ext = "jpg"
        
        save_path = filedialog.asksaveasfilename(
            defaultextension=f".{format_ext}",
            filetypes=[
                (f"{self.format_var.get()}", f"*.{format_ext}"),
                ("Todos los archivos", "*.*")
            ],
            initialfile=f"compressed_{os.path.splitext(os.path.basename(self.image_path))[0]}.{format_ext}"
        )
        
        if not save_path:
            return
        
        try:
            # Abrir y comprimir la imagen
            with Image.open(self.image_path) as img:
                # Convertir a RGB si es necesario (para JPEG)
                if self.format_var.get() == "JPEG" and img.mode in ("RGBA", "P"):
                    rgb_img = Image.new("RGB", img.size, (255, 255, 255))
                    if img.mode == "P":
                        img = img.convert("RGBA")
                    rgb_img.paste(img, mask=img.split()[3] if img.mode == "RGBA" else None)
                    img = rgb_img
                
                # Guardar con compresión
                quality = int(self.quality_slider.get())
                
                if self.format_var.get() == "PNG":
                    # PNG usa compresión sin pérdida
                    img.save(save_path, "PNG", optimize=True)
                elif self.format_var.get() == "WebP":
                    img.save(save_path, "WebP", quality=quality)
                else:  # JPEG
                    img.save(save_path, "JPEG", quality=quality, optimize=True)
            
            # Calcular reducción de tamaño
            new_size = os.path.getsize(save_path)
            reduction = ((self.original_size - new_size) / self.original_size) * 100
            new_size_mb = new_size / (1024 * 1024)
            
            messagebox.showinfo(
                "¡Éxito!",
                f"Imagen comprimida exitosamente\n\n"
                f"Tamaño original: {self.original_size / (1024 * 1024):.2f} MB\n"
                f"Tamaño nuevo: {new_size_mb:.2f} MB\n"
                f"Reducción: {reduction:.1f}%"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al comprimir la imagen:\n{str(e)}")

if __name__ == "__main__":
    app = ImageCompressor()
    app.mainloop()