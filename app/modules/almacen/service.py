from loguru import logger
# Importar la sesión de DB y la función de actualización necesaria

from app.db.database import SessionLocal
# Asume que este modelo es accesible desde esta ruta
from app.modules.inventario.models import Producto 

def actualizar_estado_producto_por_id(id_producto: str, ubicacion: str, nuevo_estado: str = "almacenado"):
    """
    Busca un producto por su ID, verifica la ubicación (opcional) y actualiza su estado.
    Retorna True si se actualizó un producto, False en caso contrario.
    """
    with SessionLocal() as db:
        # 1. Iniciar la búsqueda por el ID del producto
        query = db.query(Producto).filter(Producto.producto_id == id_producto)
        
        # Opcional: Agregar el filtro de estado anterior y ubicación para seguridad
        query = query.filter(Producto.estado == "registrado") 
        query = query.filter(Producto.ubicacion == ubicacion)
        
        producto = query.first()

      
        if producto:
            # 2. Actualizar el estado del producto
            producto.estado = nuevo_estado
            db.commit()
            logger.info(f"💾 DB: Producto {id_producto} actualizado a estado '{nuevo_estado}' en {ubicacion}.")
            return True
        
        logger.warning(f"⚠️ DB: No se encontró producto pendiente con ID {id_producto} en {ubicacion}.")
        return False


def manejador_evento_almacenamiento(device_id: str, event: str, ubicacion: str, id_producto: str = ""):
    """
    Maneja los eventos relacionados con el almacenamiento de productos.
    Implementa la lógica para actualizar el estado del producto en la DB usando su ID.
    """
    logger.info(f"[ALMACEN] Evento '{event}' recibido desde {device_id} para ID {id_producto} en ubicación {ubicacion}")
    
    # 1. Validación del evento
    if event != "almacenado":
        return {
            "status": "error",
            "message": f"Evento '{event}' no manejado por el módulo de almacenamiento.",
            "next_action": None
        }

    # 1.1. Validación de ID del producto (Nuevo)
    if not id_producto:
        logger.error("❌ ID de producto faltante en el evento de almacenamiento.")
        return {
            "status": "error",
            "message": "ID de producto faltante.",
            "next_action": None
        }
    
    # 2. Lógica principal: Actualizar el estado en la base de datos por ID
    actualizado = actualizar_estado_producto_por_id(id_producto, ubicacion=ubicacion)
    
    if not actualizado:
        logger.error(f"❌ Fallo al actualizar el estado del producto ID {id_producto}. No se encontró registro pendiente que coincida.")
        return {
            "status": "error",
            "message": f"Error: No se encontró un producto con ID {id_producto} que se pudiera marcar como almacenado en {ubicacion}.",
            "next_action": None
        }
        
    # 3. Respuesta de éxito
    logger.info(f"✅ Producto ID {id} en ubicación {ubicacion} marcado como almacenado.")
    return {
        "status": "ok",
        "message": f"Producto ID {id_producto} en ubicación {ubicacion} marcado como almacenado.",
        "next_action": "punto_0"
    }