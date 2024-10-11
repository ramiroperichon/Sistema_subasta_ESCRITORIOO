class Subasta:
    def __init__(self, nombre, fecha_inicio, fecha_fin,
                 descripcion, modo_entrega, forma_pago, estado):
        self.nombre = nombre
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.descripcion = descripcion
        self.modo_entrega = modo_entrega
        self.forma_pago = forma_pago
        self.estado = estado

    def __str__(self):
        return f"Subasta: {self.nombre} - Fecha_fin: ${self.fecha_fin} - Descripcion: ${self.descripcion}"

    


