# app/modules/communication/router.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from loguru import logger
from .controller import manejar_mensaje_entrada
import json

router = APIRouter()

# 🔹 Diccionario de conexiones activas (clave = device_id)
active_connections: dict[str, WebSocket] = {}


# =====================================================
# 🔸 Funciones auxiliares
# =====================================================

async def enviar_a_dispositivo(device_id: str, message: dict):
    """Envía un mensaje JSON a un dispositivo específico si está conectado."""
    try:
        if device_id in active_connections:
            await active_connections[device_id].send_text(json.dumps(message))
            logger.info(f"📤 Mensaje enviado a {device_id}: {message}")
        else:
            logger.warning(f"⚠️ No hay conexión activa para {device_id}")
    except Exception as e:
        logger.error(f"❌ Error enviando mensaje a {device_id}: {e}")


async def broadcast(message: dict):
    """Envía un mensaje JSON a todos los dispositivos conectados."""
    disconnected = []
    for device_id, websocket in active_connections.items():
        try:
            await websocket.send_text(json.dumps(message))
        except Exception as e:
            logger.error(f"⚠️ Error enviando broadcast a {device_id}: {e}")
            disconnected.append(device_id)

    # Limpiar conexiones caídas
    for d in disconnected:
        del active_connections[d]
        logger.warning(f"🔌 Conexión eliminada: {d}")

    logger.info(f"📢 Broadcast enviado a {len(active_connections)} dispositivos.")


# =====================================================
# 🔸 WebSocket principal del sistema
# =====================================================
@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Maneja conexiones entrantes de los microcontroladores y el HMI."""
    await websocket.accept()
    device_id = websocket.query_params.get("device_id")
    if not device_id:
        await websocket.send_text(json.dumps({"error": "Falta 'device_id' en la conexión"}))
        await websocket.close()
        return

    # Registrar conexión inmediatamente
    active_connections[device_id] = websocket
    logger.info(f"✅ Dispositivo conectado: {device_id}")

    # 🔹 1️⃣ Enviar confirmación directa al dispositivo recién conectado
    await enviar_a_dispositivo(device_id, {
        "source": "wms",
        "type": "status",
        "status": "ok",
        "message": f"Conexión establecida con el WMS como {device_id}",
    })

    # 🔹 2️⃣ Notificar a los demás (HMI u otros módulos)
    await broadcast({
        "source": "wms",
        "type": "status",
        "status": "ok",
        "message": f"Dispositivo conectado: {device_id}",
    })

    try:
        # Bucle principal: recepción de mensajes
        while True:
            raw_data = await websocket.receive_text()
            await manejar_mensaje_entrada(
                websocket,
                raw_data,
                active_connections,
                enviar_a_dispositivo,
                broadcast
            )

    except WebSocketDisconnect:
        if device_id and device_id in active_connections:
            del active_connections[device_id]
        logger.warning(f"❌ Dispositivo desconectado: {device_id}")

        # Notificar desconexión
        await broadcast({
            "source": "wms",
            "type": "status",
            "status": "warning",
            "message": f"Dispositivo desconectado: {device_id}",
        })

    except Exception as e:
        logger.error(f"⚠️ Error en conexión con {device_id}: {e}")
        if device_id and device_id in active_connections:
            del active_connections[device_id]
