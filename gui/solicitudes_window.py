import tkinter as tk
from tkinter import ttk, messagebox
from database.db_connection import fetch_solicitudes_por_subasta, update_estado_solicitud  
# from gui.product_images_window import ProductImagesWindow  

class SolicitudesWindow:
    def __init__(self, root, id_subasta):
        self.root = root
        self.root.title("Solicitudes de la Subasta")
        self.root.geometry("800x400")
        self.id_subasta = id_subasta

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
            id_solicitud, nombre, precio_base, descripcion, estado_aprobacion = solicitud

            self.tree_solicitudes.insert("", "end", iid=id_solicitud, values=(nombre, precio_base, descripcion, estado_aprobacion))

    def ver_imagenes(self):
        selected_item = self.tree_solicitudes.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una solicitud.")
            return

        id_producto = self.tree_solicitudes.item(selected_item, "values")[0] 
        new_window = tk.Toplevel(self.root)
        # ProductImagesWindow(new_window, id_producto) 

    def aceptar_solicitud(self):
        selected_item = self.tree_solicitudes.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una solicitud.")
            return

        id_solicitud = selected_item[0]
        success, msg = update_estado_solicitud(id_solicitud, "Aprobada")
        if success:
            self.load_data()
        else:
            messagebox.showerror("Error", f"No se pudo aceptar la solicitud: {msg}")

    def rechazar_solicitud(self):
      selected_item = self.tree_solicitudes.selection()
      if not selected_item:
          messagebox.showwarning("Advertencia", "Por favor, selecciona una solicitud.")
          return

      id_solicitud = selected_item[0]  # Obtener el iid, que es el id_solicitud

      success, msg = update_estado_solicitud(id_solicitud, "Rechazada")
      if success:
          self.load_data()
      else:
          messagebox.showerror("Error", f"No se pudo rechazar la solicitud: {msg}")
