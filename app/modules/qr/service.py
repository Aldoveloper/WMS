# app/modules/qr/service.py

from loguru import logger
from app.modules.inventario.service import (
    registrar_producto,
    obtener_siguiente_fifo,
    asignar_ubicacion
)

def manejador_evento_QR(device_id: str, event: str, producto_id: str):
    """
    Maneja los eventos cuando un QR es leído por el robot.
    Integra el registro del producto y la lógica FIFO.
    """
    logger.info(f"[QR] Evento '{event}' recibido desde {device_id} con ID {producto_id}")
    #validar que el producto_id no este vacio
    if not producto_id or producto_id == "sin_id":
        logger.error("❌ ID de producto inválido recibido desde el QR.")
        return {
            "status": "error",
            "message": "ID de producto inválido.",
            "next_action": None
        }
    # validar que el producto no exista ya en inventario
    existente = registrar_producto(producto_id, solo_validar=True)
    if existente:
        logger.warning(f"⚠️ El producto con ID {producto_id} ya existe en inventario.")
        return {
            "status": "error",
            "message": f"El producto con ID {producto_id} ya existe en inventario.",
            "next_action": None
        }
    
    # ✅ Registrar el producto en inventario
    producto = registrar_producto(producto_id)
    if not producto:
        logger.error(f"❌ Error registrando el producto con ID {producto_id}")
        return {
            "status": "error",
            "message": f"Error registrando el producto con ID {producto_id}.",
            "next_action": None
        }
    logger.info(f"✅ Producto {producto_id} registrado con éxito en inventario.")

    # 🧠 Lógica FIFO: obtener el siguiente producto pendiente
    # 1. Calcular la ubicación. 
    # (Usamos el ID del producto que acabamos de registrar)
    ubicacion = f"A-{producto.id:03d}"
   # 2. Asignar la ubicación en la base de datos
    asignar_ubicacion(producto.producto_id, ubicacion)
    logger.info(f"🏬 Producto {producto.producto_id} asignado a ubicación {ubicacion}")

    # 🚀 Retornar respuesta estándar
    return {
        "status": "ok",
        "message": f"QR {producto_id} registrado. Asignando ubicación {ubicacion or 'pendiente'}...",
        "ubicacion": ubicacion,
        "next_action": "start_car"
    }
