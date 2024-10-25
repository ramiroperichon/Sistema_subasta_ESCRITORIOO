import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from database.db_connection import fetch_oferentes_por_producto


class OferentesProducto:
    def __init__(self, root, id_producto):
        self.root = root
        self.root.title("Oferentes")
        self.root.geometry("900x700")
        self.id_producto = id_producto
        
        self.tree_oferentes = ttk.Treeview(self.root, columns=("col1", "col2", "col3", "col4", "col5",
                                                               "col6"), show="headings")

        self.tree_oferentes.heading("col1", text="Nombre")
        self.tree_oferentes.heading("col2", text="Apellido")
        self.tree_oferentes.heading("col3", text="Dni")
        self.tree_oferentes.heading("col4", text="Telefono")
        self.tree_oferentes.heading("col5", text="Direccion")
        self.tree_oferentes.heading("col6", text="Monto ofertado")

        self.tree_oferentes.column("col1", width=100)
        self.tree_oferentes.column("col2", width=100)
        self.tree_oferentes.column("col3", width=100)
        self.tree_oferentes.column("col4", width=200)
        self.tree_oferentes.column("col5", width=200)
        self.tree_oferentes.column("col6", width=100)
        
        self.tree_oferentes.pack(expand=True, fill="both")
        
        self.load_data()
        
    
    def load_data(self):
        for row in self.tree_oferentes.get_children():
            self.tree_oferentes.delete(row)

        oferentes = fetch_oferentes_por_producto(self.id_producto)

        if not oferentes:
            messagebox.showinfo("Oferentes", "No hay oferenets asociados a este oferente.")
            return

        for oferente in oferentes:
            id, nombre, apellido, dni, telefono, direccion, monto_ofertado = oferente  
            self.tree_oferentes.insert("", "end", values=(nombre, apellido, dni, telefono, direccion, monto_ofertado))