# app/modules/communication/controller.py
import json
from loguru import logger
from .service import procesar_evento

async def manejar_mensaje_entrada(websocket, raw_data, active_connections, enviar_a_dispositivo, broadcast):
    try:
        data = json.loads(raw_data)
        logger.info(f"📩 Mensaje recibido: {data}")

        device_id = data.get("device_id")
        event = data.get("event")

        if not device_id or not event:
            await websocket.send_text(json.dumps({
                "status": "error",
                "message": "Mensaje incompleto"
            }))
            return

        # Lógica central del sistema
        response = await procesar_evento(device_id, event, data)

        # 🔹 Redirigir respuesta según destino
        target = response.get("device_target", "all")
        if target == "all":
            await broadcast(response)
        else:
            await enviar_a_dispositivo(target, response)

    except json.JSONDecodeError:
        await websocket.send_text(json.dumps({
            "status": "error",
            "message": "Formato JSON inválido"
        }))
    except Exception as e:
        logger.error(f"Error procesando mensaje: {e}")
