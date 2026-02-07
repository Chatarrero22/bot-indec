#!/usr/bin/env python3
"""
Bot de Telegram - Indicadores Económicos Argentina
- Envía recordatorios el día que INDEC publica datos
- Consulta datos actuales (IPC, EMAE, Tipo de Cambio)

Para usar con GitHub Actions
"""

import requests
import json
import os
from datetime import datetime, date
from pathlib import Path

# ============================================================
# CONFIGURACION (se lee de variables de entorno en GitHub)
# ============================================================

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

# ============================================================
# CALENDARIO INDEC - PRIMER SEMESTRE 2026
# ============================================================

CALENDARIO_INDEC = {
    # FEBRERO 2026
    (10, 2, 2026): [
        ("📊", "IPC (Inflación)", "Enero 2026"),
        ("🧺", "Canasta Básica Alimentaria y Total", "Enero 2026"),
    ],
    (18, 2, 2026): [
        ("🏭", "Utilización Capacidad Instalada Industria", "Diciembre 2025"),
    ],
    (19, 2, 2026): [
        ("🏗️", "Indicadores Actividad Construcción (ISAC)", "Diciembre 2025"),
        ("🏭", "Índice Producción Industrial Manufacturero", "Diciembre 2025"),
    ],
    (24, 2, 2026): [
        ("📈", "EMAE (Actividad Económica)", "Diciembre 2025"),
    ],
    (25, 2, 2026): [
        ("🛒", "Encuesta de Supermercados", "Diciembre 2025"),
        ("🏪", "Encuesta Autoservicios Mayoristas", "Diciembre 2025"),
        ("🛍️", "Encuesta Centros de Compras", "Diciembre 2025"),
    ],
    (26, 2, 2026): [
        ("💼", "Índice de Salarios", "Diciembre 2025"),
    ],
    
    # MARZO 2026
    (12, 3, 2026): [
        ("📊", "IPC (Inflación)", "Febrero 2026"),
        ("🧺", "Canasta Básica Alimentaria y Total", "Febrero 2026"),
    ],
    (18, 3, 2026): [
        ("🏭", "Utilización Capacidad Instalada Industria", "Enero 2026"),
    ],
    (19, 3, 2026): [
        ("🏗️", "Indicadores Actividad Construcción (ISAC)", "Enero 2026"),
        ("🏭", "Índice Producción Industrial Manufacturero", "Enero 2026"),
    ],
    (24, 3, 2026): [
        ("📈", "EMAE (Actividad Económica)", "Enero 2026"),
    ],
    (25, 3, 2026): [
        ("🛒", "Encuesta de Supermercados", "Enero 2026"),
        ("🏪", "Encuesta Autoservicios Mayoristas", "Enero 2026"),
        ("🛍️", "Encuesta Centros de Compras", "Enero 2026"),
    ],
    (26, 3, 2026): [
        ("💼", "Índice de Salarios", "Enero 2026"),
    ],
    (31, 3, 2026): [
        ("👥", "Pobreza e Indigencia", "Segundo Semestre 2025"),
    ],
    
    # ABRIL 2026
    (15, 4, 2026): [
        ("📊", "IPC (Inflación)", "Marzo 2026"),
        ("🧺", "Canasta Básica Alimentaria y Total", "Marzo 2026"),
    ],
    (21, 4, 2026): [
        ("🏗️", "Indicadores Actividad Construcción (ISAC)", "Febrero 2026"),
        ("🏭", "Índice Producción Industrial Manufacturero", "Febrero 2026"),
    ],
    (22, 4, 2026): [
        ("📈", "EMAE (Actividad Económica)", "Febrero 2026"),
    ],
    (23, 4, 2026): [
        ("🛒", "Encuesta de Supermercados", "Febrero 2026"),
        ("🏪", "Encuesta Autoservicios Mayoristas", "Febrero 2026"),
        ("🛍️", "Encuesta Centros de Compras", "Febrero 2026"),
    ],
    (28, 4, 2026): [
        ("💼", "Índice de Salarios", "Febrero 2026"),
    ],
    
    # MAYO 2026
    (14, 5, 2026): [
        ("📊", "IPC (Inflación)", "Abril 2026"),
        ("🧺", "Canasta Básica Alimentaria y Total", "Abril 2026"),
    ],
    (20, 5, 2026): [
        ("🏗️", "Indicadores Actividad Construcción (ISAC)", "Marzo 2026"),
        ("🏭", "Índice Producción Industrial Manufacturero", "Marzo 2026"),
    ],
    (21, 5, 2026): [
        ("📈", "EMAE (Actividad Económica)", "Marzo 2026"),
    ],
    (27, 5, 2026): [
        ("🛒", "Encuesta de Supermercados", "Marzo 2026"),
        ("🏪", "Encuesta Autoservicios Mayoristas", "Marzo 2026"),
        ("🛍️", "Encuesta Centros de Compras", "Marzo 2026"),
    ],
    (28, 5, 2026): [
        ("💼", "Índice de Salarios", "Marzo 2026"),
    ],
    
    # JUNIO 2026
    (11, 6, 2026): [
        ("📊", "IPC (Inflación)", "Mayo 2026"),
        ("🧺", "Canasta Básica Alimentaria y Total", "Mayo 2026"),
    ],
    (17, 6, 2026): [
        ("🏗️", "Indicadores Actividad Construcción (ISAC)", "Abril 2026"),
        ("🏭", "Índice Producción Industrial Manufacturero", "Abril 2026"),
    ],
    (23, 6, 2026): [
        ("📈", "EMAE (Actividad Económica)", "Abril 2026"),
    ],
    (24, 6, 2026): [
        ("🛒", "Encuesta de Supermercados", "Abril 2026"),
        ("🏪", "Encuesta Autoservicios Mayoristas", "Abril 2026"),
        ("🛍️", "Encuesta Centros de Compras", "Abril 2026"),
    ],
    (25, 6, 2026): [
        ("💼", "Índice de Salarios", "Abril 2026"),
    ],
    (30, 6, 2026): [
        ("👥", "Pobreza e Indigencia", "Primer Trimestre 2026"),
    ],
}

# ============================================================
# FUNCIONES TELEGRAM
# ============================================================

def enviar_telegram(mensaje):
    """Envía mensaje por Telegram"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ Error: Faltan TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID")
        return False
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensaje,
        "parse_mode": "HTML"
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        if response.status_code == 200:
            print("✅ Mensaje enviado por Telegram")
            return True
        else:
            print(f"❌ Error Telegram: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error Telegram: {e}")
        return False

# ============================================================
# FUNCIONES DE RECORDATORIOS
# ============================================================

def obtener_proximas_publicaciones(cantidad=5):
    """Obtiene las próximas N publicaciones"""
    hoy = date.today()
    proximas = []
    
    for (dia, mes, anio), publicaciones in CALENDARIO_INDEC.items():
        fecha = date(anio, mes, dia)
        if fecha >= hoy:
            for emoji, indicador, periodo in publicaciones:
                proximas.append((fecha, emoji, indicador, periodo))
    
    proximas.sort(key=lambda x: x[0])
    return proximas[:cantidad]

def verificar_publicaciones_hoy():
    """Verifica si hay publicaciones programadas para hoy"""
    hoy = date.today()
    clave = (hoy.day, hoy.month, hoy.year)
    
    print(f"📅 Verificando publicaciones para {hoy.strftime('%d/%m/%Y')}...")
    
    if clave in CALENDARIO_INDEC:
        publicaciones = CALENDARIO_INDEC[clave]
        
        mensaje = "🔔 <b>RECORDATORIO INDEC</b>\n\n"
        mensaje += f"📅 Hoy <b>{hoy.strftime('%d/%m/%Y')}</b> se publica:\n\n"
        
        for emoji, indicador, periodo in publicaciones:
            mensaje += f"{emoji} <b>{indicador}</b>\n"
            mensaje += f"    📆 Período: {periodo}\n\n"
        
        mensaje += "⏰ Los datos se publican a las 16:00 hs\n"
        mensaje += "🔗 https://www.indec.gob.ar"
        
        print(f"📢 Hay {len(publicaciones)} publicación(es) hoy")
        return mensaje
    else:
        print("📭 No hay publicaciones programadas para hoy")
        return None

# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 50)
    print("🇦🇷 Bot Indicadores Económicos Argentina")
    print("=" * 50)
    
    hoy = date.today()
    
    # 1. Verificar si hay recordatorio para hoy
    recordatorio = verificar_publicaciones_hoy()
    
    if recordatorio:
        # Si hay publicación hoy, enviar recordatorio
        enviar_telegram(recordatorio)
    else:
        # Si NO hay publicación hoy, enviar resumen de próximas fechas
        proximas = obtener_proximas_publicaciones(5)
        
        mensaje = "🇦🇷 <b>BOT INDEC ACTIVO</b> ✅\n\n"
        mensaje += f"📅 Hoy es {hoy.strftime('%d/%m/%Y')}\n"
        mensaje += "No hay publicaciones INDEC programadas para hoy.\n\n"
        mensaje += "<b>📋 Próximas publicaciones:</b>\n\n"
        
        for fecha, emoji, indicador, periodo in proximas:
            dias_faltan = (fecha - hoy).days
            mensaje += f"{emoji} <b>{indicador}</b>\n"
            mensaje += f"    📆 {fecha.strftime('%d/%m/%Y')} (en {dias_faltan} días)\n\n"
        
        mensaje += f"🕐 {datetime.now().strftime('%H:%M')} hs"
        
        enviar_telegram(mensaje)
    
    print("=" * 50)

if __name__ == "__main__":
    main()
