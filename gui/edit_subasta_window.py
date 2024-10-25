import tkinter as tk
from tkinter import ttk, messagebox
from database.db_connection import get_db_connection, update_subasta
from models.subasta_model import Subasta

class EditSubastaWindow(tk.Toplevel):
    def __init__(self, master=None, id_subasta=None, main_window=None):
        super().__init__(master)
        self.main_window = main_window  # Referencia a la ventana principal
        self.id_subasta = id_subasta  # ID de la subasta a editar
        self.title("Editar Subasta")
        self.geometry("400x800")
        
        self.subasta = None
        self.load_subasta_data()
        self.create_widgets()

    def load_subasta_data(self):
        # Cargar los datos de la subasta desde la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT nombre, fecha_inicio, fecha_fin, descripcion, modo_entrega, forma_pago, estado FROM Subastas WHERE id = ?", (self.id_subasta,))
        result = cursor.fetchone()
        
        if result:
            self.subasta = Subasta(*result)
        else:
            messagebox.showerror("Error", "No se pudo cargar la subasta seleccionada.")
            self.destroy()

        conn.close()

    def create_widgets(self):
        # Crear las entradas con los datos precargados
        ttk.Label(self, text="Nombre:").pack(pady=5)
        self.entry_name = ttk.Entry(self)
        self.entry_name.insert(0, self.subasta.nombre)
        self.entry_name.pack(pady=5)

        ttk.Label(self, text="Fecha Inicio (YYYY-MM-DD):").pack(pady=5)
        self.entry_date_start = ttk.Entry(self)
        self.entry_date_start.insert(0, self.subasta.fecha_inicio)
        self.entry_date_start.pack(pady=5)

        ttk.Label(self, text="Fecha Fin (YYYY-MM-DD):").pack(pady=5)
        self.entry_date_end = ttk.Entry(self)
        self.entry_date_end.insert(0, self.subasta.fecha_fin)
        self.entry_date_end.pack(pady=5)

        ttk.Label(self, text="Descripción:").pack(pady=5)
        self.entry_description = ttk.Entry(self)
        self.entry_description.insert(0, self.subasta.descripcion)
        self.entry_description.pack(pady=5)

        ttk.Label(self, text="Modo de Entrega:").pack(pady=5)
        self.entry_delivery_mode = ttk.Entry(self)
        self.entry_delivery_mode.insert(0, self.subasta.modo_entrega)
        self.entry_delivery_mode.pack(pady=5)

        ttk.Label(self, text="Forma de Pago:").pack(pady=5)
        self.entry_payment_method = ttk.Entry(self)
        self.entry_payment_method.insert(0, self.subasta.forma_pago)
        self.entry_payment_method.pack(pady=5)


        btn_save = ttk.Button(self, text="Guardar Cambios", command=self.save_data)
        btn_save.pack(pady=10)

    def save_data(self):
        # Obtener los nuevos datos del formulario
        nombre = self.entry_name.get()
        fecha_inicio = self.entry_date_start.get()
        fecha_fin = self.entry_date_end.get()
        descripcion = self.entry_description.get()
        modo_entrega = self.entry_delivery_mode.get()
        forma_pago = self.entry_payment_method.get()

        # Llamar al método para actualizar los datos en la base de datos
        success, message = update_subasta(self.id_subasta, nombre, fecha_inicio, fecha_fin, descripcion, modo_entrega, forma_pago)

        if success:
            messagebox.showinfo("Éxito", message)

            # Refrescar el Treeview en la ventana principal
            if self.main_window:
                self.main_window.load_data()

            self.destroy()  # Cerrar la ventana

        else:
            messagebox.showerror("Error", message)

