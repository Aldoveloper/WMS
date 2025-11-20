# app/modules/inventario/service.py
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.modules.inventario.models import Producto
from datetime import datetime
from loguru import logger

def registrar_producto(producto_id: str, solo_validar: bool = False):
    #validar que el producto no exista ya en inventario
    if solo_validar:
        with SessionLocal() as db:
            existente = db.query(Producto).filter_by(producto_id=producto_id).first()
            return existente is not None

    """Registrar un nuevo producto detectado en la banda."""
    with SessionLocal() as db:
        producto = Producto(producto_id=producto_id)
        db.add(producto)
        db.commit()
        db.refresh(producto)
        logger.info(f"📦 Producto registrado: {producto_id}")
        return producto

def asignar_ubicacion(producto_id: str, ubicacion: str):
    """Asignar ubicación a un producto ya registrado."""
    with SessionLocal() as db:
        producto = db.query(Producto).filter_by(producto_id=producto_id).first()
        if not producto:
            logger.warning(f"⚠️ Producto {producto_id} no encontrado.")
            return None
        producto.ubicacion = ubicacion
        producto.estado = "registrado"
        db.commit()
        logger.info(f"🏬 Producto {producto_id} asignado a {ubicacion}")
        return producto

def obtener_siguiente_fifo():
    """Obtener el producto más antiguo en espera (FIFO)."""
    with SessionLocal() as db:
        producto = (
            db.query(Producto)
            .filter(Producto.estado == "almacenado")
            .order_by(Producto.timestamp.asc())
            .first()
        )
        if producto:
            logger.info(f"🔄 Siguiente en FIFO: {producto.producto_id}")
        return producto

#producto entregado, actualizar estado, cambio de estado a entregado y liberar ubicacion
def marcar_producto_entregado(producto_id: str):
    """Marcar un producto como entregado y liberar su ubicación."""
    with SessionLocal() as db:
        producto = db.query(Producto).filter_by(producto_id=producto_id).first()
        if not producto:
            logger.warning(f"⚠️ Producto {producto_id} no encontrado.")
            return None
        producto.estado = "entregado"
        producto.ubicacion = None
        db.commit()
        logger.info(f"✅ Producto {producto_id} marcado como entregado.")
        return producto
