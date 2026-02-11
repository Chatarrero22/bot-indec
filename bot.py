#!/usr/bin/env python3
"""
Bot de Telegram - Indicadores Económicos Argentina
Avisa cuando salen:
- INDEC: IPC, EMAE, IPI Manufacturero, ISAC, Supermercados
- UTDT: ICC (Confianza del Consumidor)
+ Recordatorio para actualizar PDF/Excel

Para usar con GitHub Actions
"""

import requests
import os
from datetime import datetime, date

# ============================================================
# CONFIGURACION
# ============================================================

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

# Cambiar a False cuando quieras que solo avise los días de publicación
MODO_PRUEBA = False

# ============================================================
# CALENDARIO - INDICADORES INDEC + UTDT
# ============================================================

CALENDARIO = {
    # FEBRERO 2026
    (10, 2, 2026): [
        ("📊", "IPC (Inflación)", "Enero 2026", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-5-31", "INDEC"),
    ],
    (20, 2, 2026): [
        ("😊", "ICC (Confianza Consumidor)", "Enero 2026", "https://www.utdt.edu/ver_contenido.php?id_contenido=2575&id_item_menu=4982", "UTDT"),
    ],
    (24, 2, 2026): [
        ("📈", "EMAE (Actividad Económica)", "Diciembre 2025", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-9-48", "INDEC"),
    ],
    (25, 2, 2026): [
        ("🛒", "Supermercados", "Diciembre 2025", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-1-34", "INDEC"),
    ],
    
    # MARZO 2026
    (6, 3, 2026): [
        ("🏭", "IPI Manufacturero", "Enero 2026", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-6-14", "INDEC"),
        ("🏗️", "ISAC (Construcción)", "Enero 2026", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-3-42", "INDEC"),
    ],
    (12, 3, 2026): [
        ("📊", "IPC (Inflación)", "Febrero 2026", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-5-31", "INDEC"),
    ],
    (20, 3, 2026): [
        ("🛒", "Supermercados", "Enero 2026", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-1-34", "INDEC"),
        ("😊", "ICC (Confianza Consumidor)", "Febrero 2026", "https://www.utdt.edu/ver_contenido.php?id_contenido=2575&id_item_menu=4982", "UTDT"),
    ],
    (26, 3, 2026): [
        ("📈", "EMAE (Actividad Económica)", "Enero 2026", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-9-48", "INDEC"),
    ],
    
    # ABRIL 2026
    (9, 4, 2026): [
        ("🏭", "IPI Manufacturero", "Febrero 2026", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-6-14", "INDEC"),
        ("🏗️", "ISAC (Construcción)", "Febrero 2026", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-3-42", "INDEC"),
    ],
    (15, 4, 2026): [
        ("📊", "IPC (Inflación)", "Marzo 2026", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-5-31", "INDEC"),
    ],
    (20, 4, 2026): [
        ("😊", "ICC (Confianza Consumidor)", "Marzo 2026", "https://www.utdt.edu/ver_contenido.php?id_contenido=2575&id_item_menu=4982", "UTDT"),
    ],
    (22, 4, 2026): [
        ("📈", "EMAE (Actividad Económica)", "Febrero 2026", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-9-48", "INDEC"),
    ],
    (23, 4, 2026): [
        ("🛒", "Supermercados", "Febrero 2026", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-1-34", "INDEC"),
    ],
    
    # MAYO 2026
    (7, 5, 2026): [
        ("🏭", "IPI Manufacturero", "Marzo 2026", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-6-14", "INDEC"),
        ("🏗️", "ISAC (Construcción)", "Marzo 2026", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-3-42", "INDEC"),
    ],
    (14, 5, 2026): [
        ("📊", "IPC (Inflación)", "Abril 2026", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-5-31", "INDEC"),
    ],
    (20, 5, 2026): [
        ("😊", "ICC (Confianza Consumidor)", "Abril 2026", "https://www.utdt.edu/ver_contenido.php?id_contenido=2575&id_item_menu=4982", "UTDT"),
    ],
    (21, 5, 2026): [
        ("📈", "EMAE (Actividad Económica)", "Marzo 2026", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-9-48", "INDEC"),
    ],
    (22, 5, 2026): [
        ("🛒", "Supermercados", "Marzo 2026", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-1-34", "INDEC"),
    ],
    
    # JUNIO 2026
    (9, 6, 2026): [
        ("🏭", "IPI Manufacturero", "Abril 2026", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-6-14", "INDEC"),
        ("🏗️", "ISAC (Construcción)", "Abril 2026", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-3-42", "INDEC"),
    ],
    (11, 6, 2026): [
        ("📊", "IPC (Inflación)", "Mayo 2026", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-5-31", "INDEC"),
    ],
    (19, 6, 2026): [
        ("🛒", "Supermercados", "Abril 2026", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-1-34", "INDEC"),
    ],
    (20, 6, 2026): [
        ("😊", "ICC (Confianza Consumidor)", "Mayo 2026", "https://www.utdt.edu/ver_contenido.php?id_contenido=2575&id_item_menu=4982", "UTDT"),
    ],
    (29, 6, 2026): [
        ("📈", "EMAE (Actividad Económica)", "Abril 2026", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-9-48", "INDEC"),
    ],
}

# ============================================================
# DÍAS PARA ACTUALIZAR PDF/EXCEL
# ============================================================

DIAS_ACTUALIZAR_PDF = {
    (26, 2, 2026): "Ya salieron: IPC, ICC, EMAE, Supermercados",
    (13, 3, 2026): "Ya salieron: IPI, ISAC, IPC",
    (27, 3, 2026): "Ya salieron: ICC, Supermercados, EMAE - Mes completo",
    (16, 4, 2026): "Ya salieron: IPI, ISAC, IPC",
    (24, 4, 2026): "Ya salieron: ICC, EMAE, Supermercados - Mes completo",
    (15, 5, 2026): "Ya salieron: IPI, ISAC, IPC",
    (23, 5, 2026): "Ya salieron: ICC, EMAE, Supermercados - Mes completo",
    (12, 6, 2026): "Ya salieron: IPI, ISAC, IPC",
    (30, 6, 2026): "Ya salieron: ICC, Supermercados, EMAE - Semestre completo",
}

# ============================================================
# FUNCIONES PARA OBTENER DATOS
# ============================================================

def obtener_ipc():
    """Intenta obtener IPC de múltiples fuentes"""
    try:
        url = "https://api.argentinadatos.com/v1/finanzas/indices/inflacion"
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                ultimo = data[-1]
                return f"{ultimo['valor']}% mensual"
    except:
        pass
    return None

def obtener_emae():
    """Obtiene el último dato de EMAE"""
    try:
        url = "https://apis.datos.gob.ar/series/api/series/?ids=143.3_NO_PR_2004_A_31&last=2&format=json"
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            if data.get("data") and len(data["data"]) >= 2:
                actual = data["data"][-1][1]
                anterior = data["data"][-2][1]
                if actual and anterior:
                    var = ((actual - anterior) / anterior) * 100
                    return f"Var. mensual: {var:+.1f}%"
    except:
        pass
    return None

def intentar_obtener_dato(indicador):
    """Intenta buscar el dato según el indicador"""
    if "IPC" in indicador:
        return obtener_ipc()
    elif "EMAE" in indicador:
        return obtener_emae()
    return None

def obtener_proximas_publicaciones(cantidad=5):
    """Obtiene las próximas N publicaciones"""
    hoy = date.today()
    proximas = []
    
    for (dia, mes, anio), publicaciones in CALENDARIO.items():
        try:
            fecha = date(anio, mes, dia)
            if fecha >= hoy:
                for item in publicaciones:
                    emoji, indicador, periodo, url, fuente = item
                    proximas.append((fecha, emoji, indicador, periodo, fuente))
        except:
            pass
    
    proximas.sort(key=lambda x: x[0])
    return proximas[:cantidad]

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
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        if response.status_code == 200:
            print("✅ Mensaje enviado por Telegram")
            return True
        else:
            print(f"❌ Error Telegram: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error Telegram: {e}")
        return False

# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 50)
    print("🇦🇷 Bot Indicadores Económicos Argentina")
    print(f"🔧 Modo prueba: {'ACTIVADO' if MODO_PRUEBA else 'DESACTIVADO'}")
    print("=" * 50)
    
    hoy = date.today()
    clave = (hoy.day, hoy.month, hoy.year)
    
    print(f"📅 Fecha: {hoy.strftime('%d/%m/%Y')}")
    
    mensajes_enviados = 0
    
    # 1. Verificar si hay publicación hoy
    if clave in CALENDARIO:
        publicaciones = CALENDARIO[clave]
        
        mensaje = "🔔 <b>HOY SALE DATO</b>\n\n"
        
        for item in publicaciones:
            emoji, indicador, periodo, url, fuente = item
            
            mensaje += f"{emoji} <b>{indicador}</b>\n"
            mensaje += f"    📆 Período: {periodo}\n"
            mensaje += f"    🏛️ Fuente: {fuente}\n"
            
            # Intentar buscar dato (solo INDEC tiene APIs)
            if fuente == "INDEC":
                dato = intentar_obtener_dato(indicador)
                if dato:
                    mensaje += f"    📊 {dato}\n"
                else:
                    mensaje += f"    ⏳ Dato disponible ~16:00 hs\n"
            else:
                mensaje += f"    🔗 <a href='{url}'>Ver en {fuente}</a>\n"
            
            mensaje += "\n"
        
        if any(item[4] == "INDEC" for item in publicaciones):
            mensaje += "⏰ INDEC publica a las 16:00 hs"
        
        print(f"📢 Publicaciones hoy: {len(publicaciones)}")
        enviar_telegram(mensaje)
        mensajes_enviados += 1
    
    # 2. Verificar si es día de actualizar PDF
    if clave in DIAS_ACTUALIZAR_PDF:
        motivo = DIAS_ACTUALIZAR_PDF[clave]
        
        mensaje = "📋 <b>RECORDATORIO: ACTUALIZAR PDF/EXCEL</b>\n\n"
        mensaje += f"📅 {hoy.strftime('%d/%m/%Y')}\n\n"
        mensaje += f"✅ {motivo}\n\n"
        mensaje += "💡 Pedile a Claude que actualice el reporte."
        
        print(f"📋 Día de actualizar PDF")
        enviar_telegram(mensaje)
        mensajes_enviados += 1
    
    # 3. Modo prueba
    if mensajes_enviados == 0 and MODO_PRUEBA:
        print("🧪 Modo prueba activado")
        
        proximas = obtener_proximas_publicaciones(5)
        
        mensaje = "✅ <b>BOT ACTIVO</b>\n\n"
        mensaje += f"📅 Hoy: {hoy.strftime('%d/%m/%Y')}\n"
        mensaje += "No hay publicaciones hoy.\n\n"
        mensaje += "<b>Próximos datos:</b>\n\n"
        
        for fecha, emoji, indicador, periodo, fuente in proximas:
            dias = (fecha - hoy).days
            mensaje += f"{emoji} {indicador} ({fuente})\n"
            mensaje += f"    📅 {fecha.strftime('%d/%m')} ({dias} días)\n\n"
        
        enviar_telegram(mensaje)
    
    elif mensajes_enviados == 0:
        print("📭 No hay publicaciones ni recordatorios hoy")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
