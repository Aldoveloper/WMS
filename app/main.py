# app/main.py
from fastapi import FastAPI
from app.modules.comunicacion.router import router as comm_router
from app.modules.inventario.router import router as inventario_router
from app.db.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware




# Crear tablas en la base de datos al iniciar
Base.metadata.create_all(bind=engine)

app = FastAPI(title="WMS Orquestador - Sistema Modular")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(comm_router)
app.include_router(inventario_router)

# Para ejecutar:
# uvicorn app.main:app --reload
