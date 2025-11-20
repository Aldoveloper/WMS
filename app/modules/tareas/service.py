from loguru import logger


def manejador_evento_tareas(device_id: str, event: str, id_producto: str):
    """Manejador especializado para eventos relacionados con tareas."""
    logger.info(f"🔧 Manejando evento de tareas desde {device_id}: {event} para producto {id_producto}")
    # Lógica específica para manejar eventos de tareas
    if event == "asignar_tarea":
        # Lógica para asignar una tarea relacionada con el producto
        logger.info(f"✅ Tarea asignada para el producto {id_producto} desde {device_id}")
        return {
            "status": "ok",
            "message": f"Tarea asignada para el producto {id_producto}.",
            "next_action": "iniciar_tarea"
        }
    else:
        logger.warning(f"⚠️ Evento de tarea desconocido: {event} desde {device_id}")
        return {
            "status": "error",
            "message": f"Evento de tarea '{event}' no manejado.",
            "next_action": None
        }
    