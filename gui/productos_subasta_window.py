import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database.db_connection import fetch_productos_por_subasta

class ProductosSubastaWindow:
    def __init__(self, root, id_subasta):
        self.root = root
        self.root.title("Productos de la Subasta")
        self.root.geometry("600x400")

        self.tree_productos = ttk.Treeview(self.root, columns=("col1", "col2", "col3", "col4"), show="headings")

        self.tree_productos.heading("col1", text="Nombre")
        self.tree_productos.heading("col2", text="Precion base")
        self.tree_productos.heading("col3", text="Descripcion")
        self.tree_productos.heading("col4", text="Estado")

        self.tree_productos.column("col1", width=100)
        self.tree_productos.column("col2", width=100)
        self.tree_productos.column("col3", width=200)
        self.tree_productos.column("col4", width=100)

        self.tree_productos.pack(expand=True, fill="both")

        self.load_productos(id_subasta)

    def load_productos(self, id_subasta):
        productos = fetch_productos_por_subasta(id_subasta)

        if not productos:
            messagebox.showinfo("Productos", "No hay productos asociados a esta subasta.")
            return

        for producto in productos:
            nombre, precio_base, descripcion, estado = producto  # Descomponer la tupla
            estado_str = "Disponible" if estado == 1 else "No Disponible"  # Si tienes un campo de estado
            self.tree_productos.insert("", "end", values=(nombre, precio_base, descripcion, estado_str))
