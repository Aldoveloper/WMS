# WMS Orquestador – Sistema de Automatización en Tiempo Real

Sistema encargado de coordinar microcontroladores (bandas, robots, ESP32-CAM) mediante WebSockets, gestionando el flujo de productos dentro del inventario bajo una arquitectura FIFO. Incluye un backend en FastAPI, una base de datos local SQLite y un HMI en React para monitoreo.

---

## 🚀 Descripción del Sistema

El WMS-Orquestador centraliza la comunicación entre dispositivos, manejando eventos en tiempo real como detección de productos, lectura de QR, asignación de ubicaciones y actualización del inventario. Todo el inventario se almacena en una base de datos local SQLite, permitiendo operar en redes sin internet.

---

## 🏗️ Arquitectura

- **WebSocket** para comunicación bidireccional en tiempo real.
- **Módulo Banda:** Detecta productos listos.
- **Módulo QR:** Procesa códigos leídos por los robots.
- **Módulo Robot:** Interactúa con el flujo de transporte.
- **Inventario FIFO:** Registra, ordena y asigna ubicaciones.
- **API REST:** Permite consultar y administrar el inventario.
- **SQLite** como base de datos ligera y local.
- **HMI en React:** Panel para enviar eventos y visualizar respuestas.

---

## 🛠️ Tecnologías Utilizadas

- Python 3.11+
- FastAPI
- WebSockets
- SQLAlchemy
- SQLite
- Loguru
- React + Vite
- ESP32 / Microcontroladores

---

## 📦 Instalación

1. Clonar el repositorio:

```bash
git clone  https://github.com/Aldoveloper/WMS.git
cd orquestador

---

