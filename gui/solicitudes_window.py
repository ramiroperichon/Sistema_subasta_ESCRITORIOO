import io
import tkinter as tk
from azure.storage.blob import BlobServiceClient
from tkinter import Image, ttk, messagebox
import webbrowser 
from PIL import Image, ImageTk
from database.db_connection import fetch_solicitudes_por_subasta, update_estado_solicitud, fetch_imagenes_producto

class SolicitudesWindow:
    def __init__(self, root, id_subasta):
        self.root = root
        self.root.title("Solicitudes de la Subasta")
        self.root.geometry("800x400")
        self.id_subasta = id_subasta
        self.blob_service_client = BlobServiceClient(account_url="https://imagenesproducto.blob.core.windows.net/imagenes", credential="O4xStjmODbOKRQ8Mj8LVrtDEl/I/VhU05IMXWdYYMMgZRgYGD6GEcMJl28cW9wYemrnlMeyBYhzT+AStBr9rqg")
        self.container_client = self.blob_service_client.get_container_client("imagenesproducto")

        self.create_widgets()

    def create_widgets(self):
        self.tree_solicitudes = ttk.Treeview(self.root, columns=("col1", "col2", "col3", "col4"),
                                             show="headings")

        self.tree_solicitudes.heading("col1", text="Producto")
        self.tree_solicitudes.heading("col2", text="Precio Base")
        self.tree_solicitudes.heading("col3", text="Descripcion")
        self.tree_solicitudes.heading("col4", text="Estado Aprobacion")

        self.tree_solicitudes.column("col1", width=200)
        self.tree_solicitudes.column("col2", width=250)
        self.tree_solicitudes.column("col3", width=150)
        self.tree_solicitudes.column("col4", width=150)
        
        self.tree_solicitudes.pack(expand=True, fill="both")

        # Frame para los botones
        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=10)

        # Botón para ver imágenes del producto
        btn_ver_imagenes = tk.Button(frame_botones, text="Ver Imágenes", command=self.ver_imagenes)
        btn_ver_imagenes.pack(side="left", padx=5)

        # Botón para aceptar la solicitud
        btn_aceptar_solicitud = tk.Button(frame_botones, text="Aceptar Solicitud", command=self.aceptar_solicitud)
        btn_aceptar_solicitud.pack(side="left", padx=5)

        # Botón para rechazar la solicitud
        btn_rechazar_solicitud = tk.Button(frame_botones, text="Rechazar Solicitud", command=self.rechazar_solicitud)
        btn_rechazar_solicitud.pack(side="left", padx=5)

        self.load_data()

    def load_data(self):
        for row in self.tree_solicitudes.get_children():
            self.tree_solicitudes.delete(row)

        solicitudes = fetch_solicitudes_por_subasta(self.id_subasta)

        for solicitud in solicitudes:
            id_producto, nombre, precio_base, descripcion, estado_aprobacion = solicitud

            self.tree_solicitudes.insert("", "end", iid=id_producto, values=(nombre, precio_base, descripcion, estado_aprobacion))

    def ver_imagenes(self):
        selected_item = self.tree_solicitudes.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una solicitud.")
            return

        id_producto = selected_item[0]
        
        imagenes = fetch_imagenes_producto(id_producto)
        if not imagenes:
            messagebox.showinfo("Info", "No hay imágenes disponibles para este producto.")
            return

        new_window = tk.Toplevel(self.root)
        new_window.title("Imágenes del Producto")
        new_window.geometry("800x600")

        for imagen in imagenes:
            imagen = Image.open(imagen)
            imagen = imagen.resize((200, 200)) 
            img_tk = ImageTk.PhotoImage(imagen)

            lbl_imagen = tk.Label(new_window, imagen=img_tk)
            lbl_imagen.imagen = img_tk  
            lbl_imagen.pack(pady=10)

    def aceptar_solicitud(self):
        selected_item = self.tree_solicitudes.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una solicitud.")
            return

        id_producto = selected_item[0]
        success, msg = update_estado_solicitud(id_producto, "Aprobada")
        if success:
            self.load_data()
        else:
            messagebox.showerror("Error", f"No se pudo aceptar la solicitud: {msg}")

    def rechazar_solicitud(self):
        selected_item = self.tree_solicitudes.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una solicitud.")
            return

        id_producto = selected_item[0]  

        success, msg = update_estado_solicitud(id_producto, "Rechazada")
        if success:
            self.load_data()
        else:
            messagebox.showerror("Error", f"No se pudo rechazar la solicitud: {msg}")


    def descargar_imagen(self, ruta):
        blob_client = self.container_client.get_blob_client(ruta)
        blob_data = blob_client.download_blob().readall()
        return Image.open(io.BytesIO(blob_data))