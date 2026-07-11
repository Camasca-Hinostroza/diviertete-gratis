# backend/scraper.py
import requests
from bs4 import BeautifulSoup  # 👈 El cerebro extractor que lee etiquetas HTML
from backend.database import conectar_base_datos
import os

def ejecutar_bot_recolector_html():
    print("🤖 El robot cazador está escaneando la estructura HTML por red...")
    
    # Apuntamos a la ruta virtual que acabamos de publicar en tu servidor local
    puerto = os.environ.get("PORT", "8000")
    url_fuente = "http://127.0.0.1:8000/fuente-oficial"
    
    try:
        respuesta = requests.get(url_fuente, timeout=10)
        if respuesta.status_code != 200:
            print(f"❌ Error al acceder a la página fuente: {respuesta.status_code}")
            return
            
        # Pasamos el HTML crudo descargado por el extractor BeautifulSoup
        sopa = BeautifulSoup(respuesta.text, 'html.parser')
        
        # 🎯 CAZA MAYOR: Buscamos todos los contenedores con la clase "tarjeta-evento"
        tarjetas = sopa.find_all('div', class_='tarjeta-evento')
        print(f"📸 Se encontraron {len(tarjetas)} eventos en el HTML.")
        
    except Exception as e:
        print(f"❌ Error de conexión en el scraping: {e}")
        return

    conexion = conectar_base_datos()
    if not conexion: return
    cursor = conexion.cursor()

    try:
        for tarjeta in tarjetas:
            # Extrayendo los atributos de datos (atributos personalizados del HTML)
            distrito = tarjeta.get('data-distrito')
            categoria = tarjeta.get('data-categoria')
            
            # Extrayendo los textos internos buscando por etiquetas específicas
            titulo = tarjeta.find('h2', class_='titulo-oficial').text.strip()
            descripcion = tarjeta.find('p', class_='descripcion-corta').text.strip()
            fecha = tarjeta.find('span', class_='fecha').text.strip()
            hora = tarjeta.find('span', class_='hora').text.strip()
            lugar = tarjeta.find('p', class_='direccion').text.strip()

            # 1. Asegurar o registrar Categoría en SQLite
            cursor.execute("SELECT id FROM categorias WHERE nombre = ?", (categoria,))
            cat = cursor.fetchone()
            id_categoria = cat["id"] if cat else cursor.execute("INSERT INTO categorias (nombre) VALUES (?)", (categoria,)).lastrowid

            # 2. Asegurar o registrar Distrito en SQLite
            cursor.execute("SELECT id FROM distritos WHERE nombre = ?", (distrito,))
            dist = cursor.fetchone()
            id_distrito = dist["id"] if dist else cursor.execute("INSERT INTO distritos (nombre) VALUES (?)", (distrito,)).lastrowid

            # 3. Guardar en la tabla eventos evitando duplicados por título
            cursor.execute("SELECT id FROM eventos WHERE titulo = ?", (titulo,))
            if not cursor.fetchone():
                query_insert = """
                    INSERT INTO eventos (titulo, descripcion, lugar_direccion, fecha_evento, hora_evento, id_distrito, id_categoria, estado)
                    VALUES (?, ?, ?, ?, ?, ?, ?, 'activos')
                """
                cursor.execute(query_insert, (titulo, descripcion, lugar, fecha, hora, id_distrito, id_categoria))
                print(f"🔥 ¡Raspado e Inyectado exitosamente!: {titulo}")

        conexion.commit()
        print("🤖 Scraping avanzado completado. Base de datos SQLite sincronizada.")

    except Exception as e:
        print(f"❌ Error al inyectar el scraping en SQLite: {e}")
    finally:
        cursor.close()
        conexion.close()

if __name__ == "__main__":
    ejecutar_bot_recolector_html()