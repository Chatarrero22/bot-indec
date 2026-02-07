# 🇦🇷 Bot Indicadores Económicos Argentina

Bot de Telegram que envía recordatorios cuando INDEC publica datos económicos.

## 📋 Indicadores incluidos

- 📊 IPC (Inflación)
- 🧺 Canasta Básica Alimentaria y Total
- 📈 EMAE (Actividad Económica)
- 🛒 Supermercados
- 🏪 Autoservicios Mayoristas
- 🛍️ Centros de Compras
- 💼 Índice de Salarios
- 🏗️ Construcción (ISAC)
- 🏭 Producción Industrial
- 👥 Pobreza e Indigencia

## ⚙️ Configuración

### Paso 1: Crear repositorio en GitHub

1. Andá a [github.com](https://github.com) y logueate
2. Click en **"New repository"** (o el botón + arriba a la derecha)
3. Nombre: `bot-indec` (o el que quieras)
4. Dejalo **público** o **privado** (como prefieras)
5. Click en **"Create repository"**

### Paso 2: Subir los archivos

Subí estos 3 archivos a tu repositorio:
- `bot.py`
- `requirements.txt`
- `.github/workflows/bot-diario.yml`

Podés hacerlo arrastrando los archivos a la web de GitHub o usando git.

### Paso 3: Configurar los Secrets (MUY IMPORTANTE)

1. En tu repositorio, andá a **Settings** → **Secrets and variables** → **Actions**
2. Click en **"New repository secret"**
3. Agregá estos 2 secrets:

| Name | Value |
|------|-------|
| `TELEGRAM_BOT_TOKEN` | `8138400157:AAHObBmjtLr0QrT2R66eRL8793NCtU2NqpE` |
| `TELEGRAM_CHAT_ID` | `6779507640` |

### Paso 4: Activar GitHub Actions

1. Andá a la pestaña **Actions** en tu repositorio
2. Si te pide habilitar workflows, hacé click en **"I understand my workflows, go ahead and enable them"**

### Paso 5: Probar manualmente

1. En **Actions**, seleccioná el workflow **"Bot INDEC Diario"**
2. Click en **"Run workflow"** → **"Run workflow"**
3. Esperá ~30 segundos y revisá tu Telegram

## ⏰ Horario de ejecución

El bot corre automáticamente todos los días a las **6:00 AM Argentina** (9:00 UTC).

Solo te envía mensaje cuando hay una publicación INDEC programada para ese día.

## 📱 Ejemplo de mensaje

```
🔔 RECORDATORIO INDEC

📅 Hoy 10/02/2026 se publica:

📊 IPC (Inflación)
    📆 Período: Enero 2026

🧺 Canasta Básica Alimentaria y Total
    📆 Período: Enero 2026

⏰ Los datos se publican a las 16:00 hs
🔗 https://www.indec.gob.ar
```

## 📅 Calendario cargado

Actualmente tiene cargado el calendario del **primer semestre 2026**.

Para actualizar el calendario del segundo semestre, editá el diccionario `CALENDARIO_INDEC` en `bot.py`.

## 🔧 Correr localmente (opcional)

```bash
export TELEGRAM_BOT_TOKEN="tu_token"
export TELEGRAM_CHAT_ID="tu_chat_id"
python bot.py
```
