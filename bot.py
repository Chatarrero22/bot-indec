#!/usr/bin/env python3
"""
Bot de Telegram - Indicadores Económicos Argentina
Avisa cuando salen: IPC, ICC, EMAE, IPI Manufacturero, ISAC, Supermercados
Intenta buscar el dato, si no lo encuentra manda el link igual

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
MODO_PRUEBA = True
# ============================================================
# CALENDARIO - SOLO LOS INDICADORES QUE SEGUIMOS
# ============================================================

CALENDARIO_INDEC = {
    # FEBRERO 2026
    (10, 2, 2026): [
        ("📊", "IPC (Inflación)", "Enero 2026", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-5-31"),
    ],
    (19, 2, 2026): [
        ("🏗️", "ICC (Costo Construcción)", "Enero 2026", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-5-33"),
    ],
    (24, 2, 2026): [
        ("📈", "EMAE (Actividad Económica)", "Diciembre 2025", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-9-48"),
    ],
    (25, 2, 2026): [
        ("🛒", "Supermercados", "Diciembre 2025", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-1-34"),
    ],
    
    # MARZO 2026
    (6, 3, 2026): [
        ("🏭", "IPI Manufacturero", "Enero 2026", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-6-14"),
        ("🏗️", "ISAC (Construcción)", "Enero 2026", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-3-42"),
    ],
    (12, 3, 2026): [
        ("📊", "IPC (Inflación)", "Febrero 2026", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-5-31"),
    ],
    (17, 3, 2026): [
        ("🏗️", "ICC (Costo Construcción)", "Febrero 2026", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-5-33"),
    ],
    (20, 3, 2026): [
        ("🛒", "Supermercados", "Enero 2026", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-1-34"),
    ],
    (26, 3, 2026): [
        ("📈", "EMAE (Actividad Económica)", "Enero 2026", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-9-48"),
    ],
    
    # ABRIL 2026
    (9, 4, 2026): [
        ("🏭", "IPI Manufacturero", "Febrero 2026", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-6-14"),
        ("🏗️", "ISAC (Construcción)", "Febrero 2026", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-3-42"),
    ],
    (15, 4, 2026): [
        ("📊", "IPC (Inflación)", "Marzo 2026", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-5-31"),
    ],
    (16, 4, 2026): [
        ("🏗️", "ICC (Costo Construcción)", "Marzo 2026", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-5-33"),
    ],
    (22, 4, 2026): [
        ("📈", "EMAE (Actividad Económica)", "Febrero 2026", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-9-48"),
    ],
    (23, 4, 2026): [
        ("🛒", "Supermercados", "Febrero 2026", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-1-34"),
    ],
    
    # MAYO 2026
    (7, 5, 2026): [
        ("🏭", "IPI Manufacturero", "Marzo 2026", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-6-14"),
        ("🏗️", "ISAC (Construcción)", "Marzo 2026", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-3-42"),
    ],
    (14, 5, 2026): [
        ("📊", "IPC (Inflación)", "Abril 2026", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-5-31"),
    ],
    (19, 5, 2026): [
        ("🏗️", "ICC (Costo Construcción)", "Abril 2026", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-5-33"),
    ],
    (21, 5, 2026): [
        ("📈", "EMAE (Actividad Económica)", "Marzo 2026", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-9-48"),
    ],
    (22, 5, 2026): [
        ("🛒", "Supermercados", "Marzo 2026", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-1-34"),
    ],
    
    # JUNIO 2026
    (9, 6, 2026): [
        ("🏭", "IPI Manufacturero", "Abril 2026", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-6-14"),
        ("🏗️", "ISAC (Construcción)", "Abril 2026", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-3-42"),
    ],
    (11, 6, 2026): [
        ("📊", "IPC (Inflación)", "Mayo 2026", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-5-31"),
    ],
    (17, 6, 2026): [
        ("🏗️", "ICC (Costo Construcción)", "Mayo 2026", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-5-33"),
    ],
    (19, 6, 2026): [
        ("🛒", "Supermercados", "Abril 2026", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-1-34"),
    ],
    (29, 6, 2026): [
        ("📈", "EMAE (Actividad Económica)", "Abril 2026", "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-9-48"),
    ],
}

# ============================================================
# FUNCIONES PARA OBTENER DATOS (opcional, si falla no pasa nada)
# ============================================================

def intentar_obtener_dato(indicador):
    """Intenta buscar el dato, si falla devuelve None"""
    try:
        if "IPC" in indicador:
            url = "https://api.argentinadatos.com/v1/finanzas/indices/inflacion"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data:
                    return f"{data[-1]['valor']}% mensual"
        
        elif "EMAE" in indicador:
            url = "https://apis.datos.gob.ar/series/api/series/?ids=143.3_NO_PR_2004_A_31&last=2&format=json"
            response = requests.get(url, timeout=10)
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

def obtener_proximas_publicaciones(cantidad=5):
    """Obtiene las próximas N publicaciones"""
    hoy = date.today()
    proximas = []
    
    for (dia, mes, anio), publicaciones in CALENDARIO_INDEC.items():
        try:
            fecha = date(anio, mes, dia)
            if fecha >= hoy:
                for emoji, indicador, periodo, url in publicaciones:
                    proximas.append((fecha, emoji, indicador, periodo))
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
            print(f"❌ Error Telegram: {response.status_code} - {response.text}")
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
    
    if clave in CALENDARIO_INDEC:
        # HAY PUBLICACIÓN HOY
        publicaciones = CALENDARIO_INDEC[clave]
        
        mensaje = "🔔 <b>HOY SALE DATO INDEC</b>\n\n"
        
        for emoji, indicador, periodo, url in publicaciones:
            mensaje += f"{emoji} <b>{indicador}</b>\n"
            mensaje += f"    📆 Período: {periodo}\n"
            
            # Intentar buscar dato (si falla, no pasa nada)
            dato = intentar_obtener_dato(indicador)
            if dato:
                mensaje += f"    📊 {dato}\n"
            
            mensaje += f"    🔗 <a href='{url}'>Ver en INDEC</a>\n\n"
        
        mensaje += "⏰ Publicación: 16:00 hs"
        
        print(f"📢 Publicaciones hoy: {len(publicaciones)}")
        enviar_telegram(mensaje)
        
    elif MODO_PRUEBA:
        # MODO PRUEBA - enviar resumen
        print("🧪 Modo prueba activado")
        
        proximas = obtener_proximas_publicaciones(5)
        
        mensaje = "✅ <b>BOT ACTIVO</b>\n\n"
        mensaje += f"📅 Hoy: {hoy.strftime('%d/%m/%Y')}\n"
        mensaje += "No hay publicaciones hoy.\n\n"
        mensaje += "<b>Próximos datos:</b>\n\n"
        
        for fecha, emoji, indicador, periodo in proximas:
            dias = (fecha - hoy).days
            mensaje += f"{emoji} {indicador}\n"
            mensaje += f"    📅 {fecha.strftime('%d/%m')} ({dias} días)\n\n"
        
        enviar_telegram(mensaje)
        
    else:
        print("📭 No hay publicaciones hoy")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
