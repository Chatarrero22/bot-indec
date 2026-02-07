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
# FUNCIONES DE DATOS
# ============================================================

def obtener_tipo_cambio():
    """Tipo de cambio de DolarApi"""
    try:
        response = requests.get("https://dolarapi.com/v1/dolares/oficial", timeout=30)
        response.raise_for_status()
        data = response.json()
        return {
            "venta": data.get("venta"),
            "compra": data.get("compra"),
            "fecha": data.get("fechaActualizacion", "")[:10]
        }
    except Exception as e:
        print(f"   Error tipo cambio: {e}")
        return None

def obtener_ipc():
    """IPC de ArgentinaDatos"""
    try:
        response = requests.get(
            "https://api.argentinadatos.com/v1/finanzas/indices/inflacion",
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                ultimo = data[-1]
                
                # Calcular acumulado 12 meses
                inflacion_12m = sum(d.get("valor", 0) for d in data[-12:])
                
                return {
                    "fecha": ultimo.get("fecha", "")[:7],
                    "valor": ultimo.get("valor"),
                    "acumulado_12m": inflacion_12m
                }
    except Exception as e:
        print(f"   Error IPC: {e}")
    return None

def obtener_emae():
    """EMAE de datos.gob.ar"""
    try:
        response = requests.get(
            "https://apis.datos.gob.ar/series/api/series/",
            params={
                "ids": "143.3_NO_PR_2004_A_31:percent_change_a_year_ago,143.3_NO_PR_2004_A_31:percent_change",
                "last": 1,
                "format": "json"
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("data") and len(data["data"]) > 0:
                ultimo = data["data"][0]
                return {
                    "fecha": ultimo[0][:7] if ultimo[0] else "",
                    "var_interanual": ultimo[1],
                    "var_mensual": ultimo[2]
                }
    except Exception as e:
        print(f"   Error EMAE: {e}")
    return None

def formatear_fecha(fecha_str):
    """Formatea fecha YYYY-MM a Mes Año"""
    if not fecha_str or len(fecha_str) < 7:
        return fecha_str
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    try:
        anio, mes = fecha_str[:7].split("-")
        return f"{meses[int(mes)-1]} {anio}"
    except:
        return fecha_str

def formatear_variacion(valor):
    """Formatea variación con signo"""
    if valor is None:
        return "N/D"
    if abs(valor) < 0.05:
        return "0.0%"
    signo = "+" if valor > 0 else ""
    return f"{signo}{valor:.1f}%"

def generar_resumen_datos():
    """Genera resumen de datos actuales"""
    print("\n📊 Consultando datos actuales...")
    
    mensaje = "🇦🇷 <b>DATOS ECONÓMICOS ARGENTINA</b>\n\n"
    
    # Tipo de cambio
    tc = obtener_tipo_cambio()
    if tc and tc["venta"]:
        mensaje += f"💵 <b>Tipo de Cambio Oficial</b>\n"
        mensaje += f"   Venta: ${tc['venta']:.2f} | Compra: ${tc['compra']:.2f}\n\n"
    
    # IPC
    ipc = obtener_ipc()
    if ipc and ipc["valor"]:
        mensaje += f"📊 <b>IPC (Inflación)</b> - {formatear_fecha(ipc['fecha'])}\n"
        mensaje += f"   Mensual: {ipc['valor']:.1f}%\n"
        if ipc.get("acumulado_12m"):
            mensaje += f"   Acumulado 12 meses: {ipc['acumulado_12m']:.1f}%\n\n"
    
    # EMAE
    emae = obtener_emae()
    if emae:
        mensaje += f"📈 <b>EMAE (Actividad)</b> - {formatear_fecha(emae['fecha'])}\n"
        mensaje += f"   Var. interanual: {formatear_variacion(emae.get('var_interanual'))}\n"
        mensaje += f"   Var. mensual: {formatear_variacion(emae.get('var_mensual'))}\n\n"
    
    mensaje += f"🕐 {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    
    return mensaje

# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 50)
    print("🇦🇷 Bot Indicadores Económicos Argentina")
    print("=" * 50)
    
    # 1. Verificar si hay recordatorio para hoy
    recordatorio = verificar_publicaciones_hoy()
    
    if recordatorio:
        # Si hay publicación hoy, enviar recordatorio
        enviar_telegram(recordatorio)
    else:
        # Si no hay publicación, enviar resumen de datos (opcional)
        # Descomentar la siguiente línea si querés recibir datos todos los días:
        # resumen = generar_resumen_datos()
        # enviar_telegram(resumen)
        print("💤 No hay nada que enviar hoy")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
