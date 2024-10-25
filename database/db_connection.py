import pyodbc

def get_db_connection():
    conn = pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=.;'    
        'DATABASE=sistema_subastas2;'   
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
        

def update_subasta(id_subasta, nombre, fecha_inicio, fecha_fin, descripcion, modo_entrega, forma_pago):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE Subastas
            SET nombre = ?, fecha_inicio = ?, fecha_fin = ?, descripcion = ?, modo_entrega = ?, forma_pago = ?
            WHERE id = ?
        """, (nombre, fecha_inicio, fecha_fin, descripcion, modo_entrega, forma_pago, id_subasta))

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
        SELECT p.id, p.nombre, p.precio_base, p.descripcion, p.estado
        FROM Productos p
        WHERE p.SubastaId = ? AND p.EstadoSolicitud = 'Aprobada'
		GROUP BY p.id, p.nombre, p.precio_base, p.descripcion, p.estado

        """
        
        cursor.execute(query, id_subasta)
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
        SELECT p.id, p.nombre, p.precio_base, p.descripcion, p.EstadoSolicitud
        FROM Productos p
        WHERE p.SubastaId = ? AND p.EstadoSolicitud != 'Aprobada'
        """
        cursor.execute(query, (id_subasta,))
        
        solicitudes = cursor.fetchall()

        cursor.close()
        conn.close()

        return solicitudes

    except Exception as e:
        print(f"Error al obtener las solicitudes de la subasta: {e}")
        return []

def update_estado_solicitud(id_producto, nuevo_estado):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        if nuevo_estado == "Aprobada":
            estado_aprobacion = "Aprobada"
        elif nuevo_estado == "Rechazada":
            estado_aprobacion = "Rechazada"

        query = """
        UPDATE Productos
        SET EstadoSolicitud = ?
        WHERE id = ?
        """
        
        cursor.execute(query, (estado_aprobacion, id_producto))
        conn.commit()

        return True, "Solicitud actualizada con éxito."

    except Exception as e:
        return False, f"Error al actualizar la solicitud: {str(e)}"

    finally:
        cursor.close()
        conn.close()


def fetch_imagenes_producto(id_producto):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        SELECT Urls FROM Productos WHERE id = ?;
        """
        cursor.execute(query, (id_producto,))
        imagenes = cursor.fetchall()
        urls = imagenes[0]
        
        return urls

    except Exception as e:
        print(f"Error al obtener las imágenes: {e}")
        return []

    finally:
        cursor.close()
        conn.close()

        
def fetch_ganancia_por_subasta(id_subasta):
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT 
                s.nombre AS nombre_subasta,
                SUM(mejor_oferta) AS suma_mejor_oferta
            FROM 
                Subastas s
            JOIN 
                (SELECT 
                     p.SubastaId,
                     MAX(o.monto) AS mejor_oferta
                 FROM 
                     Productos p
                 LEFT JOIN 
                     Ofertas o ON p.id = o.id_producto
                 GROUP BY 
                     p.id, p.SubastaId) AS sub
            ON 
                s.id = sub.SubastaId
            WHERE 
                s.id = ?
            GROUP BY 
                s.id, s.nombre;
            """
        cursor.execute(query, (id_subasta))
        
        informe = cursor.fetchall()
        return informe

    except Exception as e:
        print(f"Error al obtener el informe de ganancia por subasta: {e}")
        return []

    finally:
        cursor.close()
        conn.close()

def fetch_productos_vendidos(id_subasta):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        SELECT 
            p.nombre AS producto,
            p.precio_base,
            MAX(o.monto) AS mejor_oferta,
            (MAX(o.monto) * 0.1) AS ganancia_empresa,
            (MAX(o.monto) * 0.9) AS ganancia_vendedor
        FROM 
            Productos p
        INNER JOIN 
            Ofertas o ON p.id = o.id_producto
        WHERE 
            p.SubastaId = ?
        GROUP BY 
            p.id, p.nombre, p.precio_base
        """

        cursor.execute(query, (id_subasta,))
        productos_vendidos = cursor.fetchall()
        
        return productos_vendidos

    except Exception as e:
        print(f"Error al obtener productos vendidos: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def fetch_productos_no_vendidos(id_subasta):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        SELECT 
            p.nombre AS producto,
            p.precio_base
        FROM 
            Productos p
        LEFT JOIN 
            Ofertas o ON p.id = o.id_producto
        WHERE 
            p.SubastaId = ? AND o.id IS NULL
        """

        cursor.execute(query, (id_subasta,))
        productos_no_vendidos = cursor.fetchall()
        
        return productos_no_vendidos

    except Exception as e:
        print(f"Error al obtener productos no vendidos: {e}")
        return None
    finally:
        cursor.close()
        conn.close()
        
def fetch_informe_ofertas(id_subasta):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        SELECT 
            p.id AS producto_id,
            p.nombre,
            p.precio_base,
            p.descripcion,
            p.estado,
            COUNT(o.id) AS numero_ofertas
        FROM 
            Productos p
        LEFT JOIN 
            Ofertas o ON p.id = o.id_producto
        WHERE 
            p.SubastaId = ?
        GROUP BY 
            p.id, p.nombre, p.precio_base, p.descripcion, p.estado
        """

        cursor.execute(query, (id_subasta,))
        informe_ofertas = cursor.fetchall()
        
        return informe_ofertas

    except Exception as e:
        print(f"Error al obtener productos no vendidos: {e}")
        return None
    finally:
        cursor.close()
        conn.close()
    


def fetch_oferentes_por_producto(id_producto):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        SELECT 
            u.id AS usuario_id,
            u.nombre,
            u.apellido,
            u.dni,
            u.telefono,
            u.direccion,
            o.monto AS oferta
        FROM 
            Ofertas o
        JOIN 
            Usuarios u ON o.id_usuario = u.id
        WHERE 
            o.id_producto = ?

        """

        cursor.execute(query, (id_producto))
        oferentes = cursor.fetchall()
        
        return oferentes

    except Exception as e:
        print(f"Error al obtener los oferentes: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def cambiar_estado_subasta(id_subasta, estado):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            UPDATE Subastas
            SET estado = ? 
            WHERE id = ?
        """
        
        cursor.execute(query, (estado, id_subasta))
        conn.commit()

    except Exception as e:
        print(f"Error al actualizar el estado de la subasta: {e}")
        return None
    finally:
        cursor.close()
        conn.close()
        
        
def update_estado_producto(id_producto, nuevo_estado):
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            UPDATE Productos SET estado = ? WHERE id = ?
        """
        
        cursor.execute(query, (nuevo_estado, id_producto))
        conn.commit()

    except Exception as e:
        print(f"Error al actualizar el estado del producto: {e}")
        return None
    finally:
        cursor.close()
        conn.close()
        
def fetch_resultados(id_subasta):
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
           SELECT 
                p.id AS producto_id,
                p.nombre AS producto_nombre,
                u.nombre AS ganador_nombre,
                u.apellido AS ganador_apellido,
                u.telefono AS telefono_ganador,
                u.direccion AS direccion_ganador,
                o.monto AS oferta_ganadora
            FROM 
                Productos p
            JOIN 
                Ofertas o ON p.id = o.id_producto
            JOIN 
                Usuarios u ON o.id_usuario = u.id
            WHERE 
                p.SubastaId = ?  
                AND o.id = (SELECT TOP 1 id FROM Ofertas WHERE id_producto = p.id ORDER BY monto DESC)

        """
        
        cursor.execute(query, (id_subasta))
        resultados = cursor.fetchall()
        
        return resultados

    except Exception as e:
        print(f"Error al obtener los resultados de la subasta: {e}")
        return None
    finally:
        cursor.close()
        conn.close()
        
def fetch_dni_usuario(id_producto):
    
        
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT u.dni
            FROM Productos p
            JOIN Usuarios u ON p.IdUsuario = u.id
            WHERE p.id = ?

        """
        
        cursor.execute(query, (id_producto))
        resultados = cursor.fetchone()
        
        return resultados[0]

    except Exception as e:
        print(f"Error al obtener los resultados de la subasta: {e}")
        return None
    finally:
        cursor.close()
        conn.close()
        
def fetch_cant_oferentes(id_producto):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT COUNT(o.id) AS numero_ofertas
            FROM Productos p
            JOIN Ofertas o ON p.id = o.id_producto
            WHERE p.id = ?
        """
        
        cursor.execute(query, (id_producto))
        resultados = cursor.fetchone()
        
        return resultados[0]

    except Exception as e:
        print(f"Error al obtener los resultados de la subasta: {e}")
        return None
    finally:
        cursor.close()
        conn.close()