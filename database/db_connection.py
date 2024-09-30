import pyodbc

def get_db_connection():
    conn = pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=.;'    
        'DATABASE=sistema_subastas;'   
    )
    return conn

def fetch_all_subastas():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT id, nombre, fecha_inicio, fecha_fin, descripcion, modo_entrega, forma_pago FROM Subastas"
    
    cursor.execute(query)
    subastas = cursor.fetchall() 
    
    conn.close()
    return subastas

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