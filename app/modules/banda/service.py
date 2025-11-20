# app/modules/da/service.py

from loguru import logger

def manejador_evento_banda(device_id: str, event: str,):
    """
    Maneja los eventos provenientes de la banda transportadora.
    """
    logger.info(f"[BANDA] Evento recibido desde {device_id}: {event}")

    if event != "producto_listo":
        return {
            "status": "error",
            "message": f"Evento '{event}' no manejado por el módulo de banda.",
            "next_action": None
        }

    # Lógica principal del evento "producto_listo"
    logger.info("✅ Producto listo detectado, esperando lectura de QR por parte del robot.")
    return {
        "status": "ok",
        "message": "Producto listo. Esperando lectura de QR.",
        "next_action": "read_qr"
    }
