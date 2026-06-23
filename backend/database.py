# backend/database.py
import sqlite3

DATABASE_NAME = "cartelera.db"

def conectar_base_datos():
    """Establece conexión con SQLite y activa el modo diccionario para Jinja2"""
    try:
        conexion = sqlite3.connect(DATABASE_NAME)
        conexion.row_factory = sqlite3.Row  # 👈 Crucial para mapear por nombres de columna
        return conexion
    except Exception as e:
        print(f"❌ Error al conectar a SQLite: {e}")
        return None

def inicializar_sistema_tablas():
    """Crea la estructura del imperio digital: categorías, distritos, eventos y monetización"""
    conexion = conectar_base_datos()
    if not conexion: return
    cursor = conexion.cursor()
    
    try:
        # Tabla 1: Categorías
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE NOT NULL
            )
        """)
        
        # Tabla 2: Distritos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS distritos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE NOT NULL
            )
        """)
        
        # Tabla 3: Eventos principales
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS eventos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descripcion TEXT,
                lugar_direccion TEXT,
                fecha_evento TEXT,
                hora_evento TEXT,
                id_distrito INTEGER,
                id_categoria INTEGER,
                estado TEXT DEFAULT 'activos',
                FOREIGN KEY(id_distrito) REFERENCES distritos(id),
                FOREIGN KEY(id_categoria) REFERENCES categorias(id)
            )
        """)

        # 💰 TABLA 4: NUEVA TABLA DE MONETIZACIÓN CORPORATIVA
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS billetera_monetizacion (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                impresiones_totales INTEGER DEFAULT 0,
                clics_totales INTEGER DEFAULT 0,
                saldo_acumulado_usd REAL DEFAULT 0.00
            )
        """)

        # Inicializamos la billetera en 0 si está vacía
        cursor.execute("SELECT COUNT(*) as total FROM billetera_monetizacion")
        if cursor.fetchone()["total"] == 0:
            cursor.execute("INSERT INTO billetera_monetizacion (impresiones_totales, clics_totales, saldo_acumulado_usd) VALUES (0, 0, 0.00)")

        conexion.commit()
        print("💾 Base de datos e infraestructura de monetización listas de forma persistente.")
    except Exception as e:
        print(f"❌ Error al inicializar tablas: {e}")
    finally:
        cursor.close()
        conexion.close()

def obtener_cartelera_filtrada(categoria_nombre=None):
    """Consulta a SQLite uniendo tablas para entregar los datos limpios al index.html"""
    conexion = conectar_base_datos()
    if not conexion: return []
    cursor = conexion.cursor()
    
    query = """
        SELECT eventos.id, eventos.titulo, eventos.descripcion, eventos.lugar_direccion, 
               eventos.fecha_evento, eventos.hora_evento,
               categorias.nombre as categoria_nombre, distritos.nombre as distrito_nombre
        FROM eventos
        JOIN categorias ON eventos.id_categoria = categorias.id
        JOIN distritos ON eventos.id_distrito = distritos.id
        WHERE eventos.estado = 'activos'
    """
    
    try:
        if categoria_nombre:
            query += " AND categorias.nombre = ?"
            cursor.execute(query, (categoria_nombre,))
        else:
            cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(f"❌ Error en consulta de cartelera: {e}")
        return []
    finally:
        cursor.close()
        conexion.close()

def obtener_evento_por_id(evento_id):
    """Busca los detalles de un único evento en SQLite para la vista evento.html"""
    conexion = conectar_base_datos()
    if not conexion: return None
    cursor = conexion.cursor()
    
    query = """
        SELECT eventos.id, eventos.titulo, eventos.descripcion, eventos.lugar_direccion, 
               eventos.fecha_evento, eventos.hora_evento,
               categorias.nombre as categoria_nombre, distritos.nombre as distrito_nombre
        FROM eventos
        JOIN categorias ON eventos.id_categoria = categorias.id
        JOIN distritos ON eventos.id_distrito = distritos.id
        WHERE eventos.id = ?
    """
    try:
        cursor.execute(query, (evento_id,))
        return cursor.fetchone()
    except Exception as e:
        print(f"❌ Error al obtener evento {evento_id}: {e}")
        return None
    finally:
        cursor.close()
        conexion.close()

# 🌟 NUEVAS FUNCIONES DE MONETIZACIÓN PARA TU BACKEND
def registrar_impresion_anuncio():
    """Cada vez que una página carga, sumamos una impresión y acumulamos micro-centavos de dólar"""
    conexion = conectar_base_datos()
    if not conexion: return
    cursor = conexion.cursor()
    try:
        # Simulamos que cada impresión de página nos paga $0.005 dólares ($5 de CPM)
        cursor.execute("""
            UPDATE billetera_monetizacion 
            SET impresiones_totales = impresiones_totales + 1,
                saldo_acumulado_usd = saldo_acumulado_usd + 0.005
            WHERE id = 1
        """)
        conexion.commit()
    finally:
        cursor.close()
        conexion.close()

def obtener_estado_billetera():
    """Devuelve los datos de ganancias acumuladas para mostrarlos en el panel"""
    conexion = conectar_base_datos()
    if not conexion: return {"impresiones_totales": 0, "saldo_acumulado_usd": 0.00}
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT * FROM billetera_monetizacion WHERE id = 1")
        fila = cursor.fetchone()
        return dict(fila) if fila else {"impresiones_totales": 0, "saldo_acumulado_usd": 0.00}
    finally:
        cursor.close()
        conexion.close()

# Inicialización automática al importar
inicializar_sistema_tablas()

def registrar_clic_anuncio():
    """Suma un clic al contador e inyecta $0.20 centavos de dólar premium al saldo"""
    conexion = conectar_base_datos()
    if not conexion: return
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            UPDATE billetera_monetizacion 
            SET clics_totales = clics_totales + 1,
                saldo_acumulado_usd = saldo_acumulado_usd + 0.20
            WHERE id = 1
        """)
        conexion.commit()
        print("💰 ¡PUM! ¡Un usuario hizo clic en el banner! Se han sumado $0.20 USD.")
    finally:
        cursor.close()
        conexion.close()