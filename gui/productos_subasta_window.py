import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database.db_connection import fetch_cant_oferentes, fetch_dni_usuario, fetch_oferentes_por_producto, fetch_productos_por_subasta, update_estado_producto
from gui.oferentes_producto_window import OferentesProducto

class ProductosSubastaWindow:
    def __init__(self, root, id_subasta):
        self.root = root
        self.root.title("Productos de la Subasta")
        self.root.geometry("700x480")

        self.tree_productos = ttk.Treeview(self.root, columns=("col1", "col2", "col3", "col4", "col5", "col6"), show="headings")

        self.tree_productos.heading("col1", text="Nombre")
        self.tree_productos.heading("col2", text="Precio base")
        self.tree_productos.heading("col3", text="Descripción")
        self.tree_productos.heading("col4", text="Dni Usuario")
        self.tree_productos.heading("col5", text="Estado")
        self.tree_productos.heading("col6", text="Oferentes")

        self.tree_productos.column("col1", width=100)
        self.tree_productos.column("col2", width=100)
        self.tree_productos.column("col3", width=200)
        self.tree_productos.column("col4", width=100)
        self.tree_productos.column("col5", width=100)
        self.tree_productos.column("col6", width=50)

        self.tree_productos.pack(expand=True, fill="both")
        
        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=10)

        # Botón para ver los oferentes
        btn_ver_oferentes = tk.Button(frame_botones, text="Oferentes", command=self.ver_oferentes)
        btn_ver_oferentes.pack(side="left", padx=5)

        # Botón para cambiar el estado del producto
        btn_cambiar_estado = tk.Button(frame_botones, text="Cambiar Estado", command=self.cambiar_estado)
        btn_cambiar_estado.pack(side="left", padx=5)

        self.load_productos(id_subasta)

    def load_productos(self, id_subasta):
        productos = fetch_productos_por_subasta(id_subasta)
        
        

        if not productos:
            messagebox.showinfo("Productos", "No hay productos asociados a esta subasta.")
            return

        for producto in productos:
            id, nombre, precio_base, descripcion, estado= producto
            dniUsuario = fetch_dni_usuario(id)  
            cantOferentes = fetch_cant_oferentes(id)     
            estado_str = "Disponible" if estado == 1 else "No Disponible"  
            self.tree_productos.insert("", "end", iid=id, values=(nombre, precio_base, descripcion, dniUsuario, estado_str, cantOferentes))

    def ver_oferentes(self):
        selected_item = self.tree_productos.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un producto.")
            return
        
        id_producto = selected_item[0]
    
        new_window = tk.Toplevel(self.root)
        OferentesProducto(new_window, id_producto)
        
    def cambiar_estado(self):
        try:
            selected_item = self.tree_productos.selection()
            if not selected_item:
                messagebox.showwarning("Advertencia", "Por favor, selecciona un producto.")
                return

            id_producto = selected_item[0]

            current_values = self.tree_productos.item(id_producto, "values")
            estado_actual = current_values[3]

            nuevo_estado = 0 if estado_actual == "Disponible" else 1

            update_estado_producto(id_producto, nuevo_estado)

            estado_str = "Disponible" if nuevo_estado == 1 else "No Disponible"
            self.tree_productos.item(id_producto, values=(current_values[0], current_values[1], current_values[2], estado_str, current_values[4]))

            messagebox.showinfo("Estado actualizado", f"El estado del producto ha sido cambiado a '{estado_str}'.")

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")



