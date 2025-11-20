# app/db/init_db.py
from app.db.database import Base, engine
from app.modules.inventario.models import Producto

print("🗄️ Creando base de datos local SQLite...")
Base.metadata.create_all(bind=engine)
print("✅ Tablas creadas exitosamente.")
print("🗄️ Base de datos inicializada.")