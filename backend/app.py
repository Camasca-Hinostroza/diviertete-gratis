# backend/app.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
# Importamos las nuevas funciones matemáticas y de lectura de saldos
from backend.database import (
    obtener_cartelera_filtrada, 
    obtener_evento_por_id,
    registrar_impresion_anuncio,
    obtener_estado_billetera,
    registrar_clic_anuncio
)

app = FastAPI(title="Diviértete Gratis API")

templates = Jinja2Templates(directory="frontend/templates")
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

@app.get("/", response_class=HTMLResponse)
def mostrar_cartelera(request: Request, categoria: str = None):
    """Ruta principal: Registra la impresión del anuncio y lee la billetera en vivo"""
    
    # 💰 MONETIZACIÓN AUTOMÁTICA: Cada carga suma $0.005 dólares a tu base de datos
    registrar_impresion_anuncio()
    
    # Extraemos el estado actual del dinero y las impresiones acumuladas
    billetera = obtener_estado_billetera()
    
    lista_eventos = obtener_cartelera_filtrada(categoria_nombre=categoria)
    
    if not lista_eventos:
        lista_eventos = [{
            "id": 0,
            "titulo": f"Sin eventos en {categoria or 'esta sección'}",
            "descripcion": "Nuestros bots están recolectando las mejores misiones y eventos gratuitos de esta categoría. ¡Regresa pronto!",
            "lugar_direccion": "Puntos estratégicos de la ciudad",
            "fecha_evento": "Fin de semana",
            "hora_evento": "Todo el día",
            "categoria_nombre": categoria or "Cultura",
            "distrito_nombre": "Lima"
        }]
    
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={
            "eventos": lista_eventos, 
            "categoria_actual": categoria,
            "billetera": billetera # 🌟 Enviamos las métricas de dinero directo a tu HTML
        }
    )

@app.get("/evento/{evento_id}", response_class=HTMLResponse)
def mostrar_detalle_evento(request: Request, evento_id: int):
    """Ruta de detalles: También monetiza la vista del usuario en evento.html"""
    
    # 💰 Si miran el detalle de un evento, también se imprime publicidad y cobramos
    registrar_impresion_anuncio()
    
    evento = obtener_evento_por_id(evento_id=evento_id)
    
    if not evento:
        return RedirectResponse(url="/")
        
    return templates.TemplateResponse(
        request=request, 
        name="evento.html", 
        context={"evento": evento}
    )

@app.get("/fuente-oficial", response_class=HTMLResponse)
def servicio_fuente_cultural_virtual():
    """Simula la página web externa de una municipalidad de Lima usando texto crudo"""
    html_externo = """
    <!DOCTYPE html>
    <html>
    <head><meta charset="UTF-8"><title>Agenda Cultural Oficial</title></head>
    <body>
        <h1>Eventos Gratuitos de la Semana</h1>
        <div class="tarjeta-evento" data-distrito="Miraflores" data-categoria="Cine">
            <h2 class="titulo-oficial">Cine Clásico en el Parque Central</h2>
            <p class="descripcion-corta">Proyección de películas antiguas al aire libre. Trae tu silla.</p>
            <span class="fecha">2026-07-20</span> <span class="hora">19:00</span>
            <p class="direccion">Anfiteatro del Parque Kennedy</p>
        </div>
        <div class="tarjeta-evento" data-distrito="Los Olivos" data-categoria="Ferias">
            <h2 class="titulo-oficial">Feria de Libros Usados</h2>
            <p class="descripcion-corta">Ven a cambiar tus novelas y textos universitarios gratis.</p>
            <span class="fecha">2026-07-22</span> <span class="hora">10:00</span>
            <p class="direccion">Explanada Municipal de Los Olivos</p>
        </div>
        <div class="tarjeta-evento" data-distrito="Lima" data-categoria="Bailables">
            <h2 class="titulo-oficial">Clases Abiertas de Marinera Limeña</h2>
            <p class="descripcion-corta">Aprende los pasos básicos de nuestra danza bandera gratis.</p>
            <span class="fecha">2026-07-25</span> <span class="hora">16:30</span>
            <p class="direccion">Plaza San Martín</p>
        </div>
    </body>
    </html>
    """
    return html_externo


@app.get("/click-publicidad")
def procesar_clic_publicitario():
    """Ruta oculta que cobra el dinero del clic y manda al usuario a Google"""
    registrar_clic_anuncio()
    # Redirigimos al usuario a una página externa (simulando la web del anunciante)
    return RedirectResponse(url="https://www.google.com")
