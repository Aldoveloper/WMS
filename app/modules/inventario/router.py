# app/modules/inventario/router.py
from fastapi import APIRouter
from app.db.database import SessionLocal
from app.modules.inventario.models import Producto
from app.modules.inventario.service import obtener_siguiente_fifo

router = APIRouter(prefix="/inventario", tags=["Inventario"])

@router.get("/listar")
def listar_productos():
    """
    Devuelve la lista completa del inventario.
    """
    with SessionLocal() as db:
        productos = db.query(Producto).all()
        return [
            {
                "id": p.id,
                "producto_id": p.producto_id,
                "estado": p.estado,
                "ubicacion": p.ubicacion,
                "timestamp": p.timestamp.isoformat()
            }
            for p in productos
        ]

# ============================================================
# 🧠 NUEVO ENDPOINT FIFO
# ============================================================
@router.get("/fifo")
def obtener_producto_fifo():
    """
    Devuelve el siguiente producto en la cola FIFO.
    Ideal para que el robot consulte qué producto debe recoger o despachar.
    """
    producto = obtener_siguiente_fifo()

    if not producto:
        return {
            "status": "empty",
            "message": "No hay productos pendientes en el inventario FIFO.",
            "producto": None
        }

    return {
        "status": "ok",
        "message": f"Siguiente producto en FIFO: {producto.producto_id}",
        "producto": {
            "id": producto.id,
            "producto_id": producto.producto_id,
            "estado": producto.estado,
            "ubicacion": producto.ubicacion,
            "timestamp": producto.timestamp.isoformat()
        }
    }
