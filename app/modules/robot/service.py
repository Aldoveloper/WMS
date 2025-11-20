def manejador_evento_robot(device_id, event, data):
    if event != "producto_listo":
        return {
            "device_id": device_id,
            "status": "error",
            "message": f"Evento '{event}' no manejado por el módulo de robot.",
            "next_action": None
        }

    return {
        
        "device_id" :device_id,
        "message" :"Producto listo. Esperando lectura de QR.",
        "next_action" :"esperar_qr"
    }