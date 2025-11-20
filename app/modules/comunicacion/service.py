# app/modules/communication/service.py
from datetime import datetime, timezone
from loguru import logger

# Futuras importaciones (cuando estén listos los módulos)
# from app.modules.inventario.service import manejador_evento_inventario
from app.modules.robot.service import manejador_evento_robot
from app.modules.almacen.service import manejador_evento_almacenamiento
from app.modules.tareas.service import manejador_evento_tareas
from app.modules.banda.service import manejador_evento_banda
from app.modules.qr.service import manejador_evento_QR




# ============================================================
# 🔹 Función base para generar respuestas uniformes
# ============================================================
def build_response(
    device_id: str,
    status: str = "ok",
    message: str = "",
    next_action: str | None = None,
    type_: str = "response",
    ubicacion: str | None = None,
    id_producto: str | None = None,  

):
    """Crea una respuesta estándar compatible con microcontroladores y HMI."""
    return {
        "source": "wms",
        "device_target": device_id,
        "type": type_,
        "ubicacion": ubicacion,
        "id_producto": id_producto,
        "status": status,
        "message": message,
        "next_action": next_action,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ============================================================
# 🔹 Lógica principal del módulo de comunicación
# ============================================================
async def procesar_evento(device_id: str, event: str, data: dict,  ):

    id_producto = data.get("id_producto", "")
    ubicacion = data.get("ubicacion", "desconocida")

    """
    Procesa el evento recibido desde un microcontrolador.
    Redirige la lógica al módulo correspondiente según el tipo de evento.
    """
    #logger.info(f"📡 [{device_id}] Evento recibido: {event}")

    match event:
        # ----------------------------------------------------
        # 🚚 Banda transportadora
        # ----------------------------------------------------
        case "producto_listo":
            #logger.info("✅ Producto detectado en la banda transportadora.")
            
            # Llamamos al manejador del módulo banda
            response = manejador_evento_banda(device_id, event)

            # Extraer datos del manejador (si devuelve dict)
            if isinstance(response, dict):
                return build_response(
                    device_id=device_id,
                    message=response.get("message", "Producto listo. Esperando lectura de QR."),
                    next_action=response.get("next_action", "read_qr"),
                    status=response.get("status", "ok"),
                )
            else:
                # fallback si el manejador devuelve solo texto
                return build_response(
                    device_id=device_id,
                    message=str(response),
                    next_action="read_qr", 
                )

        # ----------------------------------------------------
        # 🤖 Robot / Cámara (ESP32-CAM)
        # ----------------------------------------------------
        case "qr_leido":
          
            logger.info(f"🔍 Código QR leído por {device_id}: {id_producto}")

            # Llamar al manejador especializado del QR
            response = manejador_evento_QR(device_id, event, id_producto)

            # Si el manejador devuelve un dict, procesar normalmente
            if isinstance(response, dict):
                return build_response(
                    device_id=device_id,
                    message=response.get("message", f"QR {id_producto} recibido y registrado."),
                    next_action=response.get("next_action", "start_car"),
                    status=response.get("status", "ok"),
                    ubicacion=response.get("ubicacion", None),
                    id_producto=response.get(id_producto, None),
                )

            # Fallback si devuelve solo texto
            return build_response(
                device_id=device_id,
                message=str(response),
                next_action="start_car",
                ubicacion=response.get("ubicacion", None),
                id_producto=response.get(id_producto, None),
            )
        
        # ----------------------------------------------------
        # 🏬 Producto listo para almacenar
        # ----------------------------------------------------
        case "almacenar":
            ubicacion = data.get("ubicacion", "desconocida")
            logger.info(f"📦 Ubicación libre detectada: {ubicacion}")
            return build_response(
                device_id=device_id,
                message=f"Ubicación {ubicacion}.",
                next_action="actualizar_mapa"
            )
        
        # ----------------------------------------------------
        # 🏬 Producto almacenado
        # ----------------------------------------------------
        case "almacenado":
            logger.info(f"📥 Evento de almacenamiento recibido para ID {id_producto} en {ubicacion}.")
             # Llamar al manejador especializado de inventario
            response = manejador_evento_almacenamiento(device_id, event, ubicacion, id_producto)
            return build_response(
                device_id=device_id,
                message=response.get("message", "Producto almacenado correctamente."),
                next_action=response.get("next_action", None),
                status=response.get("status", "ok"),
            )
        
         # ----------------------------------------------------
        # ⚙️ Eventos robot despachar producto
        # ----------------------------------------------------
        case "despachado":
            #tenemos que enviarlo al robot para que lo despache
            logger.info(f"🤖 Producto {id_producto} despachado desde {ubicacion}."
                            )
            # Llamar al manejador especializado del robot
            response = manejador_evento_tareas(device_id, event, id_producto)
            return build_response(
                device_id=device_id,
                message=response.get("message", "Producto despachado correctamente."),
                next_action=response.get("next_action", None),
                status=response.get("status", "ok"),
            )   

        # ----------------------------------------------------
        # ⚙️ Eventos internos o administrativos
        # ----------------------------------------------------
        case "ping":
            return build_response(
                device_id=device_id,
                message="Conexión activa.",
                next_action=None
            )

        # ----------------------------------------------------
        # 🚨 Evento no reconocido
        # ----------------------------------------------------
        case _:
            logger.warning(f"⚠️ Evento desconocido: {event}")
            return build_response(
                device_id=device_id,
                status="error",
                message=f"Evento '{event}' no reconocido por el servidor.",
                next_action=None
            )
