from datetime import datetime
from database.db_connection import get_db_connection, insert_subasta
from models.subasta_model import Subasta
import tkinter as tk
from tkinter import ttk, messagebox

class CreateSubastaWindow(tk.Toplevel):
    def __init__(self, master=None, main_window=None):
        super().__init__(master)
        self.main_window = main_window
        self.title("Nueva subasta")
        self.geometry("400x800")
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Nombre:").pack(pady=5)
        self.entry_name = ttk.Entry(self)
        self.entry_name.pack(pady=5)

        ttk.Label(self, text="Fecha Inicio (YYYY-MM-DD H:M:S):").pack(pady=5)
        self.entry_date_start = ttk.Entry(self)
        self.entry_date_start.pack(pady=5)

        ttk.Label(self, text="Fecha Fin (YYYY-MM-DD H:M:S):").pack(pady=5)
        self.entry_date_end = ttk.Entry(self)
        self.entry_date_end.pack(pady=5)

        ttk.Label(self, text="Descripción:").pack(pady=5)
        self.entry_description = ttk.Entry(self)
        self.entry_description.pack(pady=5)

        ttk.Label(self, text="Modo de Entrega:").pack(pady=5)
        self.entry_delivery_mode = ttk.Combobox(self, values=["Personal", "Envio"], state="readonly")
        self.entry_delivery_mode.pack(pady=5)

        ttk.Label(self, text="Forma de Pago:").pack(pady=5)
        self.entry_payment_method = ttk.Combobox(self, values=["Transferencia", "Efectivo"], state="readonly")
        self.entry_payment_method.pack(pady=5)

        btn_save = ttk.Button(self, text="Guardar", command=self.save_data)
        btn_save.pack(pady=10)

    def save_data(self):
        nombre = self.entry_name.get()
        fecha_inicio_str = self.entry_date_start.get()
        fecha_fin_str = self.entry_date_end.get()
        descripcion = self.entry_description.get()
        modo_entrega = self.entry_delivery_mode.get()
        forma_pago = self.entry_payment_method.get()

        try:
            fecha_inicio = datetime.strptime(str(fecha_inicio_str),"%Y-%m-%d %H:%M:%S")
            fecha_fin = datetime.strptime(str(fecha_fin_str), "%Y-%m-%d %H:%M:%S")

            if fecha_fin <= fecha_inicio:
                messagebox.showerror("Error", "La fecha de fin no puede ser menor que la fecha de inicio.")
                self.entry_date_start.delete(0, tk.END)
                self.entry_date_end.delete(0, tk.END)
                return

        except ValueError as e:
            messagebox.showerror("Error", f"Formato de fecha no válido: {str(e)}")
            return

        fecha_actual = datetime.now()

        if fecha_fin > fecha_actual or fecha_inicio < fecha_actual:
            estado_subasta = 1
        else:
            estado_subasta = 0  

        success, message = insert_subasta(nombre, fecha_inicio, fecha_fin, descripcion, modo_entrega, forma_pago, estado_subasta)

        if success:
            messagebox.showinfo("Éxito", message)

            if self.main_window:
                self.main_window.load_data()

            self.destroy() 
        else:
            messagebox.showerror("Error", f"Error al guardar la subasta: {message}")

