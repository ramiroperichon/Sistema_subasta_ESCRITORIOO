from tkinter import messagebox, ttk
from database.db_connection import fetch_resultados

class ResultadosSubastaWindow:
    def __init__(self, root, id_subasta):
        self.root = root
        self.root.title("Resultados de la Subasta")
        self.root.geometry("900x600")
        self.id_subasta = id_subasta  # Guardamos el id_subasta

        # Crear el Treeview
        self.tree_resultados = ttk.Treeview(self.root, columns=("col1", "col2", "col3",
                                                                "col4", "col5", "col6"), show="headings")

        # Definir encabezados
        self.tree_resultados.heading("col1", text="Producto")
        self.tree_resultados.heading("col2", text="Ganador")
        self.tree_resultados.heading("col3", text="Apellido")
        self.tree_resultados.heading("col4", text="Teléfono")
        self.tree_resultados.heading("col5", text="Dirección")
        self.tree_resultados.heading("col6", text="Oferta Ganadora")

        # Configurar columnas
        self.tree_resultados.column("col1", width=200)
        self.tree_resultados.column("col2", width=150)
        self.tree_resultados.column("col3", width=150)
        self.tree_resultados.column("col4", width=100)
        self.tree_resultados.column("col5", width=200)
        self.tree_resultados.column("col6", width=100)

        self.tree_resultados.pack(expand=True, fill="both")

        # Cargar resultados
        self.load_resultados()

    def load_resultados(self):
       
        resultados = fetch_resultados(self.id_subasta) 

        if not resultados:
            messagebox.showinfo("Resultados", "No hay resultados para mostrar.")
            return

        # Insertar datos en el Treeview
        for resultado in resultados:
            producto_id, producto_nombre, ganador_nombre, ganador_apellido, telefono_ganador, direccion_ganador, oferta_ganadora = resultado
            
            self.tree_resultados.insert("", "end", iid=producto_id, values=(producto_nombre, ganador_nombre, ganador_apellido, telefono_ganador, direccion_ganador, oferta_ganadora))
