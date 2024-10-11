import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database.db_connection import fetch_all_subastas, update_subasta_estado
from gui.productos_subasta_window import ProductosSubastaWindow 

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Administración")
        self.root.geometry("1460x800")
        self.create_widgets()

    def create_widgets(self):
        self.tree_subastas = ttk.Treeview(self.root, columns=("col1", "col2", "col3",
                                                              "col4", "col5", "col6",
                                                              "col7"),
                                          show="headings")

        self.tree_subastas.heading("col1", text="Nombre")
        self.tree_subastas.heading("col2", text="Fecha de inicio")
        self.tree_subastas.heading("col3", text="Fecha de fin")
        self.tree_subastas.heading("col4", text="Descripción")
        self.tree_subastas.heading("col5", text="Modo de entrega")
        self.tree_subastas.heading("col6", text="Forma de pago")
        self.tree_subastas.heading("col7", text="Estado") 

       
        self.tree_subastas.column("col1", width=120)
        self.tree_subastas.column("col2", width=120)
        self.tree_subastas.column("col3", width=120)
        self.tree_subastas.column("col4", width=150)
        self.tree_subastas.column("col5", width=120)
        self.tree_subastas.column("col6", width=120)
        self.tree_subastas.column("col7", width=100) 

        self.tree_subastas.pack(side="left", expand=True, fill="both")

        # Frame para botones laterales
        frame_button_lateral = tk.Frame(self.root)
        frame_button_lateral.pack(side="right", fill="y")  

        # Botón para habilitar/deshabilitar el estado de la subasta
        btn_toggle_estado = tk.Button(frame_button_lateral, text="Habilitar/Deshabilitar Estado", command=self.toggle_estado)
        btn_toggle_estado.pack(pady=5, padx=5)

        # Botón para ver productos de la subasta
        btn_productos_subasta = tk.Button(frame_button_lateral, text="Productos", command=self.open_productos_window)
        btn_productos_subasta.pack(pady=5, padx=5)

        # Botón para editar subasta
        btn_edit_subasta = tk.Button(frame_button_lateral, text="Editar", command=self.open_edit_subasta_window)
        btn_edit_subasta.pack(pady=5, padx=5)

        btn_solicitudes_subasta = tk.Button(frame_button_lateral, text="Solicitudes", command=self.open_solicitudes_window)
        btn_solicitudes_subasta.pack(pady=5, padx=5)
        
        # Frame para botones inferiores
        frame_button_inferior = tk.Frame(self.root)
        frame_button_inferior.pack(side="bottom", pady=10)

        btn_create_subasta = tk.Button(frame_button_inferior, text="Crear",
                                       command=self.open_create_subasta_window)
        btn_create_subasta.pack(side="left", padx=10)

        btn_informes_subasta = tk.Button(frame_button_inferior, text="Informes")
        btn_informes_subasta.pack(side="right", padx=10)

        self.load_data()

    def load_data(self):
        for row in self.tree_subastas.get_children():
            self.tree_subastas.delete(row)

        subastas = fetch_all_subastas()

        for subasta in subastas:
            id_subasta = subasta[0]  
            data_visible = list(subasta[1:])  # Obtener los datos de la subasta

            # Insertar el estado correctamente sin alterar las otras columnas
            estado = "Habilitada" if data_visible[-1] == 1 else "Deshabilitada"

            # data_visible[-1] ya no se sobrescribe, sino que se añade el estado al final
            self.tree_subastas.insert("", "end", iid=id_subasta, values=(*data_visible[:-1], estado))

    def toggle_estado(self):
        selected_item = self.tree_subastas.selection()

        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una subasta.")
            return

        id_subasta = selected_item[0]

        estado_actual = self.tree_subastas.item(selected_item, "values")[6]

        nuevo_estado = 1 if estado_actual == "Deshabilitada" else 0
        nuevo_estado_str = "Habilitada" if nuevo_estado == 1 else "Deshabilitada"

        success, message = update_subasta_estado(id_subasta, nuevo_estado)

        if success:
            self.tree_subastas.item(selected_item, values=(self.tree_subastas.item(selected_item, "values")[:6] + (nuevo_estado_str,)))
            messagebox.showinfo("Éxito", "El estado de la subasta ha sido actualizado.")
        else:
            messagebox.showerror("Error", f"No se pudo actualizar el estado: {message}")

    def open_productos_window(self):
        selected_item = self.tree_subastas.selection()

        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una subasta.")
            return

        id_subasta = selected_item[0]

        new_window = tk.Toplevel(self.root)
        ProductosSubastaWindow(new_window, id_subasta)

    def open_create_subasta_window(self):
        from gui.create_subasta_window import CreateSubastaWindow
        new_window = tk.Toplevel(self.root)
        CreateSubastaWindow(new_window, main_window=self)

    def open_edit_subasta_window(self):
        selected_item = self.tree_subastas.selection()

        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una subasta para editar.")
            return

        id_subasta = selected_item[0]

        from gui.edit_subasta_window import EditSubastaWindow
        new_window = tk.Toplevel(self.root)
        EditSubastaWindow(new_window, id_subasta, main_window=self)


    def open_solicitudes_window(self):
        selected_item = self.tree_subastas.selection()
    
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una subasta.")
            return
    
        id_subasta = selected_item[0]
    
        new_window = tk.Toplevel(self.root)
        from gui.solicitudes_window import SolicitudesWindow
        SolicitudesWindow(new_window, id_subasta)
