import tkinter as tk
from tkinter import ttk

from database.db_connection import fetch_all_subastas

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Administración")
        self.root.geometry("1200x700")
        self.create_widgets()

    def create_widgets(self):
        tree_subastas = ttk.Treeview(self.root, columns=("col1", "col2", "col3",
                                                         "col4", "col5", "col6",
                                                         "col7"),
                                     show="headings")
        
        
        tree_subastas.heading("col1", text="Nombre")
        tree_subastas.heading("col2", text="Fecha de incio")
        tree_subastas.heading("col3", text="Fecha de fin")
        tree_subastas.heading("col4", text="Descripcion")
        tree_subastas.heading("col5", text="Modo de entrega")
        tree_subastas.heading("col6", text="Forma de pago")
        tree_subastas.heading("col7", text="Solicitudes")
     
      
        tree_subastas.column("col1", width=120)
        tree_subastas.column("col2", width=120)
        tree_subastas.column("col3", width=120)
        tree_subastas.column("col4", width=150)
        tree_subastas.column("col5", width=120)
        tree_subastas.column("col6", width=120)
        tree_subastas.column("col7", width=120)

        tree_subastas.pack(side="left", expand=True, fill="both")
        
        #Frame para botones laterales
        frame_button_lateral = tk.Frame(self.root)
        frame_button_lateral.pack(side="right", fill="y")  

        #Botones Laterales
        btn_productos_subasta = tk.Button(frame_button_lateral, text="Productos")
        btn_productos_subasta.pack(pady=5, padx=5)  

        btn_edit_subasta = tk.Button(frame_button_lateral, text="Editar")
        btn_edit_subasta.pack(pady=5, padx=5)

        btn_solicitudes_subasta = tk.Button(frame_button_lateral, text="Solicitudes")
        btn_solicitudes_subasta.pack(pady=5, padx=5)
        
       #Frame para botones inferiores
        frame_button_inferior = tk.Frame(self.root)
        frame_button_inferior.pack(side="bottom", pady=10)

        #Botones inferiores
        btn_create_suabasta = tk.Button(frame_button_inferior, text="Crear",
                                        command=self.open_create_subasta_window)
        btn_create_suabasta.pack(side="left", padx=10)

        btn_informes_subasta = tk.Button(frame_button_inferior, text="Informes")
        btn_informes_subasta.pack(side="right", padx=10)
        
        self.load_data(tree_subastas)

    def load_data(self, tree_subastas):
        # Borrar las filas actuales
        for row in tree_subastas.get_children():
            tree_subastas.delete(row)

        # Obtener los datos desde la base de datos
        subastas = fetch_all_subastas()

        # Insertar cada subasta en el Treeview
        for subasta in subastas:
            id_subasta = subasta[0]  # Guardar el id_subasta para uso interno
            data_visible = subasta[1:]  # Obtener el resto de los datos para mostrar
            tree_subastas.insert("", "end", iid=id_subasta, values=data_visible)


    def open_create_subasta_window(self):
        from gui.create_subasta_window import CreateSubastaWindow
        new_window = tk.Toplevel(self.root)
        CreateSubastaWindow(new_window, main_window=self)

