import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from database.db_connection import cambiar_estado_subasta, fetch_all_subastas, fetch_ganancia_por_subasta, fetch_informe_ofertas, update_subasta_estado, fetch_productos_no_vendidos, fetch_productos_vendidos
from gui.productos_subasta_window import ProductosSubastaWindow
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas 
from decimal import Decimal

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Administración")
        self.root.geometry("1460x800")
        self.create_widgets()
        self.verificar_estado_subasta()

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
        
        # Botón para refrescar
        btn_refrescar_subastas = tk.Button(frame_button_lateral, text="Refrescar", command=self.load_data)
        btn_refrescar_subastas.pack(pady=5, padx=5)
        
        #Boton para ver resultados
        btn_verificar_estado_finalizado = tk.Button(frame_button_lateral, text="Ver Resultados", command=self.verificar_estado_finalizado)
        btn_verificar_estado_finalizado.pack(pady=5, padx=5)
        
        # Frame para botones inferiores
        frame_button_inferior = tk.Frame(self.root)
        frame_button_inferior.pack(side="bottom", pady=10)

        btn_create_subasta = tk.Button(frame_button_inferior, text="Crear",
                                       command=self.open_create_subasta_window)
        btn_create_subasta.pack(side="left", padx=10)

        btn_informes_subasta = tk.Button(frame_button_inferior, text="Informes", command=self.create_informes)
        btn_informes_subasta.pack(side="right", padx=10)

        self.load_data()
        

    def load_data(self):
        for row in self.tree_subastas.get_children():
            self.tree_subastas.delete(row)

        subastas = fetch_all_subastas()

        for subasta in subastas:
            id, nombre, fecha_inicio, fecha_fin, descripcion, modo_entrega, forma_pago, estado = subasta
            
            estado = "Habilitada" if estado == 1 else "Deshabilitada"

            self.tree_subastas.insert("", "end", iid=id, values=(nombre, fecha_inicio, fecha_fin, descripcion, modo_entrega, forma_pago, estado))

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


    def draw_line(self, c, y_position, text):
        """Dibuja una línea de texto y ajusta la posición Y."""
        c.drawString(100, y_position, text)
        return y_position - 15


    def create_informes(self):
        selected_item = self.tree_subastas.selection()

        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una subasta.")
            return

        id_subasta = selected_item[0]
        informe = fetch_ganancia_por_subasta(id_subasta)

        if not informe:
            messagebox.showwarning("Advertencia", "No hay datos para generar los informes.")
            return

        nombre_subasta, ventas_totales = informe[0]
        ganancia_empresa = ventas_totales * Decimal('0.10')
        ganancia_vendedor = ventas_totales - ganancia_empresa
        fecha_informe = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.generar_informe_ganancia( nombre_subasta, ventas_totales, ganancia_empresa, fecha_informe)
        self.generar_informe_productos_no_vendidos(id_subasta, nombre_subasta, fecha_informe)
        self.generar_informe_productos_vendidos(id_subasta, nombre_subasta, fecha_informe)
        self.generar_informe_ofertas(id_subasta, nombre_subasta, fecha_informe)


    def generar_informe_ganancia(self, nombre_subasta, ventas_totales, ganancia_empresa, fecha_informe):
        cadena_replace = (nombre_subasta+"_InformeGanancias").replace(" ", "")
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], initialfile=cadena_replace)
        if not file_path:
            return  

        c = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter

        c.setFont("Helvetica-Bold", 16)
        y_position = height - 50
        c.drawString(100, y_position, f"Informe de la subasta: {nombre_subasta}")
        y_position -= 20

        c.setFont("Helvetica", 12)
        c.drawString(100, y_position, f"Fecha del informe: {fecha_informe}")
        y_position -= 20
        c.drawString(100, y_position, "Este informe refleja las ganancias globales de la empresa.")
        y_position -= 20
        c.drawString(100, y_position, "========================================")
        y_position -= 20
     
        y_position = self.draw_line(c, y_position, f"Total de ventas: {ventas_totales}")
        y_position = self.draw_line(c, y_position, f"Ganancia empresa: {ganancia_empresa}")
        y_position -= 25 

        c.save()
        messagebox.showinfo("Éxito", "Informe de ganancia generado correctamente.")

    def generar_informe_productos_no_vendidos(self, id_subasta, nombre_subasta, fecha_informe):
        cadena_replace = (nombre_subasta+"_InformeProducNoVendidos").replace(" ", "")
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], initialfile=(cadena_replace))
        if not file_path:
            return  

        c = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter

        c.setFont("Helvetica-Bold", 16)
        y_position = height - 50
        c.drawString(100, y_position, f"Resumen de productos no vendidos - Subasta: {nombre_subasta}")
        y_position -= 20
        c.setFont("Helvetica", 12)
        c.drawString(100, y_position, f"Fecha del informe: {fecha_informe}")
        y_position -= 20
        c.drawString(100, y_position, "Este informe genera todos los productos no vendidos de la subasta.")
        y_position -= 20
        c.drawString(100, y_position, "========================================")
        y_position -= 20

        productos_no_vendidos = fetch_productos_no_vendidos(id_subasta)
        for row in productos_no_vendidos:
            producto, precio_base = row
            y_position = self.draw_line(c, y_position, f"Producto: {producto}")
            y_position = self.draw_line(c, y_position, f"Precio base: {precio_base}")
            y_position -= 25 

            if y_position < 50:
                c.showPage()
                c.setFont("Helvetica", 12)
                y_position = height - 50

        c.save()
        messagebox.showinfo("Éxito", "Informe de productos no vendidos generado correctamente.")

    def generar_informe_productos_vendidos(self, id_subasta, nombre_subasta, fecha_informe):
        cadena_replace = (nombre_subasta+"_InformeProducVendidos").replace(" ", "")
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], initialfile=cadena_replace)
        if not file_path:
            return  

        c = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter

        c.setFont("Helvetica-Bold", 16)
        y_position = height - 50
        c.drawString(100, y_position, f"Resumen de productos vendidos - Subasta: {nombre_subasta}")
        y_position -= 20
        c.setFont("Helvetica", 12)
        c.drawString(100, y_position, f"Fecha del informe: {fecha_informe}")
        y_position -= 20
        c.drawString(100, y_position, "Este informe muestra todos los productos que se vendieron en la subasta.")
        y_position -= 20
        c.drawString(100, y_position, "========================================")
        y_position -= 20

        productos_vendidos = fetch_productos_vendidos(id_subasta)
        for row in productos_vendidos:
            producto, precio_base, mejor_oferta, ganancia_empresa, ganancia_vendedor = row
            y_position = self.draw_line(c, y_position, f"Producto: {producto}")
            y_position = self.draw_line(c, y_position, f"Precio base: {precio_base}")
            y_position = self.draw_line(c, y_position, f"Mejor oferta: {mejor_oferta}")
            y_position = self.draw_line(c, y_position, f"Ganancia empresa: {ganancia_empresa}")
            y_position = self.draw_line(c, y_position, f"Ganancia vendedor: {ganancia_vendedor}")

            y_position -= 25  

            if y_position < 50:
                c.showPage()
                c.setFont("Helvetica", 12)
                y_position = height - 50

        c.save()
        messagebox.showinfo("Éxito", "Informe de productos vendidos")


    def generar_informe_ofertas(self, id_subasta, nombre_subasta, fecha_informe):
         nombre_archivo = f"Resumen_Ofertas_{nombre_subasta}"
         file_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                  filetypes=[("PDF files", "*.pdf")],
                                                  initialfile=nombre_archivo,
                                                  )
         if not file_path:
             return

         c = canvas.Canvas(file_path, pagesize=letter)
         width, height = letter


         c.setFont("Helvetica-Bold", 16)
         y_position = height - 50
         c.drawString(100, y_position, f"Resumen de ofertas - Subasta: {nombre_subasta}")
         y_position -= 20
         c.setFont("Helvetica", 12)
         c.drawString(100, y_position, f"Fecha del informe: {fecha_informe}")
         y_position -= 20
         c.drawString(100, y_position, "Resumen de todas las ofertas recibidas por cada producto de la subasta.")
         y_position -= 20
         c.drawString(100, y_position, "========================================")
         y_position -= 20

         ofertas = fetch_informe_ofertas(id_subasta)
         for row in ofertas:
             id_producto, nombre, precio_base, descripcion, estado, cant_ofertas = row
             y_position = self.draw_line(c, y_position, f"Producto: {nombre}")
             y_position = self.draw_line(c, y_position, f"Descripción: {descripcion}")
             y_position = self.draw_line(c, y_position, f"Ofertas recibidas: {cant_ofertas}")
             y_position -= 25

             if y_position < 50:
                 c.showPage()
                 c.setFont("Helvetica", 12)
                 y_position = height - 50

         c.save()
         messagebox.showinfo("Éxito", "Informe de ofertas generado correctamente.")

    def verificar_estado_subasta(self): 
        
        for row in self.tree_subastas.get_children():
            values = self.tree_subastas.item(row, 'values')
            fecha_inicio_str = values[1] 
            fecha_fin_str = values[2]    

            try:
                fecha_inicio = datetime.datetime.strptime(fecha_inicio_str, "%Y-%m-%d %H:%M:%S")
                fecha_fin = datetime.datetime.strptime(fecha_fin_str, "%Y-%m-%d %H:%M:%S")

                fecha_inicio = fecha_inicio.replace(second=0, microsecond=0)
                fecha_fin = fecha_fin.replace(second=0, microsecond=0)

            except ValueError:
                print(f"Error al convertir la fecha para verificar la subasta")
                continue

            now = datetime.datetime.now().replace(second=0, microsecond=0)  
            subasta_id = row[0]

            if now >= fecha_inicio and now < fecha_fin:
               
                cambiar_estado_subasta(subasta_id, 1)
            else:
               
                cambiar_estado_subasta(subasta_id, 0) 
            
            self.load_data()

       
        self.root.after(10000, self.verificar_estado_subasta)
        
        
    def verificar_estado_finalizado(self):
        selected_item = self.tree_subastas.selection()

        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una subasta.")
            return

        subasta_id = selected_item[0]
        values = self.tree_subastas.item(subasta_id, 'values')  

        estado = values[6]  
        fecha_fin_str = values[2]  

        try:
            fecha_fin = datetime.datetime.strptime(fecha_fin_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha no válido.")
            return

        fecha_actual = datetime.datetime.now()

        if fecha_actual < fecha_fin and estado == 'Habilitada':
            messagebox.showwarning("Advertencia", "La subasta aún está activa. No se pueden generar resultados.")
            return

        if  fecha_actual < fecha_fin and estado == 'Deshabilitada': 
            messagebox.showwarning("Advertencia", "La subasta no ha finalizado. No se pueden generar resultados.")
            return

        new_window = tk.Toplevel(self.root)
        from gui.resultados_subasta_window import ResultadosSubastaWindow
        ResultadosSubastaWindow(new_window, subasta_id)

        
        
       
