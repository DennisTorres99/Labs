# Orders Service API

Servicio backend para gestión de órdenes implementado con arquitectura hexagonal (Clean Architecture) utilizando FastAPI, SQLAlchemy y Alembic.

---

##  Descripción

API REST orientada a recursos para la creación y consulta de órdenes, aplicando separación de responsabilidades en:

- Dominio
- Casos de uso
- Puertos (interfaces)
- Adaptadores (infraestructura)

Incluye documentación automática mediante Swagger.

---

##  Base URL

http://127.0.0.1:8000

---

##  Endpoints

### Crear orden

POST /orders

Parámetros:

- id: int  
- total: float  

---

### Obtener órdenes

GET /orders

---

##  Modelo de respuesta

Ejemplo:

{
  "id": 1,
  "total": 100
}

---

##  Códigos HTTP

- 200 OK  
- 201 Created  
- 400 Bad Request  
- 401 Unauthorized  
- 404 Not Found  
- 500 Internal Server Error  

---

##  Arquitectura

API → UseCase → Port → Adapter → DB

Diagrama:

graph TD
A[FastAPI API] --> B[CreateOrder]
B --> C[OrderRepository]
B --> D[Notifier]
C --> E[InMemoryRepository]
C --> F[SqlRepository]
F --> G[(SQLite)]
D --> H[HttpNotifier]

---

##  Estructura del proyecto

Proyecto/
├── domain.py  
├── use_cases.py  
├── ports.py  
├── repo_memory.py  
├── repo_sql.py  
├── notifier_http.py  
