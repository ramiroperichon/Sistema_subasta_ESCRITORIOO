import pyodbc

def get_db_connection():
    conn = pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=.;'    
        'DATABASE=sistema_subastas1;'   
    )
    return conn

def fetch_all_subastas():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT id, nombre, fecha_inicio, fecha_fin, descripcion, modo_entrega, forma_pago, estado
        FROM Subastas
        """
        
        cursor.execute(query)
        subastas = cursor.fetchall()
        
        return subastas
    
    except Exception as e:
        print(f"Error al obtener subastas: {e}")
        return []
    
    finally:
        cursor.close()
        conn.close()


def insert_subasta(nombre, fecha_inicio, fecha_fin, descripcion, modo_entrega, forma_pago, estado):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO Subastas (nombre, fecha_inicio, fecha_fin, descripcion, modo_entrega, forma_pago, estado)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (nombre, fecha_inicio, fecha_fin, descripcion, modo_entrega, forma_pago, estado))

        conn.commit()
        return True, "Subasta guardada con éxito."
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()
        

def update_subasta(id_subasta, nombre, fecha_inicio, fecha_fin, descripcion, modo_entrega, forma_pago, estado):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE Subastas
            SET nombre = ?, fecha_inicio = ?, fecha_fin = ?, descripcion = ?, modo_entrega = ?, forma_pago = ?, estado = ?
            WHERE id = ?
        """, (nombre, fecha_inicio, fecha_fin, descripcion, modo_entrega, forma_pago, estado, id_subasta))

        conn.commit()
        conn.close()
        return True, "Subasta actualizada con éxito."
    
    except Exception as e:
        return False, str(e)
    
    
def update_subasta_estado(id_subasta, nuevo_estado):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE Subastas SET estado = ? WHERE id = ?", (nuevo_estado, id_subasta))
        connection.commit()
        return True, "Estado actualizado correctamente."
    except Exception as e:
        return False, str(e)
    finally:
        cursor.close()
        connection.close()
        
def fetch_productos_por_subasta(id_subasta):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT nombre, precio_base, descripcion, estado
        FROM Productos
        WHERE SubastaId = ?
        """
        
        cursor.execute(query, (id_subasta,))
        productos = cursor.fetchall()
        
        return productos
    
    except Exception as e:
        print(f"Error al obtener los productos de la subasta: {e}")
        return []
    
    finally:
        cursor.close()
        conn.close()

def fetch_solicitudes_por_subasta(id_subasta):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        SELECT s.id, p.nombre, s.precio_base, p.descripcion, s.estado_aprobacion
        FROM Solicitudes_publicacion s
        JOIN Productos p ON s.id_producto = p.id
        WHERE p.SubastaId = ?
        """
        cursor.execute(query, (id_subasta,))
        
        solicitudes = cursor.fetchall()

        cursor.close()
        conn.close()

        return solicitudes

    except Exception as e:
        print(f"Error al obtener las solicitudes de la subasta: {e}")
        return []

def update_estado_solicitud(id_solicitud, nuevo_estado):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        if nuevo_estado == "Aprobada":
            estado_aprobacion = "Aprobada"
        elif nuevo_estado == "Rechazada":
            estado_aprobacion = "Rechazada"

        query = """
        UPDATE Solicitudes_publicacion
        SET estado_aprobacion = ?
        WHERE id = ?
        """
        
        cursor.execute(query, (estado_aprobacion, id_solicitud))
        conn.commit()

        return True, "Solicitud actualizada con éxito."

    except Exception as e:
        return False, f"Error al actualizar la solicitud: {str(e)}"

    finally:
        cursor.close()
        conn.close()


