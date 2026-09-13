# 🍔 Food Delivery Backend

A production-style REST API backend for a food-delivery platform, built with **FastAPI**.

> **Repository:** `food_delivary_backend`

## ✨ What this project demonstrates

- RESTful API design with FastAPI
- User authentication and authorization
- Restaurant management
- Food-item management
- Cart operations
- Order creation and management
- PostgreSQL database integration
- SQLAlchemy ORM
- Pydantic schemas
- Docker-based development
- Interactive API documentation
- Clean backend layering

---

## 🏗️ System Architecture

```mermaid
flowchart LR
    Client["Client / Frontend"] --> API["FastAPI Application"]

    API --> Auth["Authentication"]
    API --> Restaurant["Restaurant APIs"]
    API --> Food["Food Item APIs"]
    API --> Cart["Cart APIs"]
    API --> Order["Order APIs"]

    Auth --> DB[(PostgreSQL)]
    Restaurant --> DB
    Food --> DB
    Cart --> DB
    Order --> DB

    API --> Docs["Swagger / OpenAPI"]
```

### 🔎 Interactive architecture

For **Zoom In, Zoom Out, Pan Left/Right, Pan Up/Down, Reset and Full Screen**, open:

**[Open Interactive Architecture Viewer](./docs/architecture.html)**

GitHub renders Mermaid diagrams natively, but does not allow JavaScript controls inside `README.md`. The separate viewer provides the interactive controls.

---

# 🔄 API Request Flow

```mermaid
sequenceDiagram
    participant C as Client
    participant F as FastAPI
    participant R as Router
    participant S as Service / Logic
    participant O as SQLAlchemy ORM
    participant D as PostgreSQL

    C->>F: HTTP Request
    F->>R: Route matching
    R->>S: Validate and process request
    S->>O: Database operation
    O->>D: SQL query
    D-->>O: Database result
    O-->>S: ORM objects
    S-->>R: Response data
    R-->>F: Serialized response
    F-->>C: HTTP Response
```

**Interactive version:** [Open API Request Flow Viewer](./docs/request-flow.html)

---

# 🔐 Authentication Flow

```mermaid
sequenceDiagram
    participant U as User
    participant API as FastAPI
    participant AUTH as Auth Layer
    participant DB as PostgreSQL

    U->>API: Signup / Login
    API->>AUTH: Validate credentials
    AUTH->>DB: Read / create user
    DB-->>AUTH: User data
    AUTH-->>API: Authentication result
    API-->>U: Access token / response

    U->>API: Protected API request
    API->>AUTH: Validate token
    AUTH-->>API: Authenticated user
    API-->>U: Protected resource
```

**Interactive version:** [Open Authentication Flow Viewer](./docs/auth-flow.html)

---

# 🗃️ Database / ER Diagram

```mermaid
erDiagram
    USER ||--o{ CART : owns
    USER ||--o{ ORDER : places
    RESTAURANT ||--o{ FOOD_ITEM : offers
    CART ||--o{ FOOD_ITEM : contains
    ORDER ||--o{ ORDER_ITEM : contains
    FOOD_ITEM ||--o{ ORDER_ITEM : included_in

    USER {
        int id PK
        string name
        string email
        string password
    }

    RESTAURANT {
        int id PK
        string name
        string address
    }

    FOOD_ITEM {
        int id PK
        string name
        float price
        int restaurant_id FK
    }

    CART {
        int id PK
        int user_id FK
    }

    ORDER {
        int id PK
        int user_id FK
        string status
        float total
    }

    ORDER_ITEM {
        int id PK
        int order_id FK
        int food_item_id FK
        int quantity
    }
```

**Interactive version:** [Open ER Diagram Viewer](./docs/er-diagram.html)

---

# 🛒 Cart Workflow

```mermaid
flowchart LR
    A["User"] --> B["Select Food"]
    B --> C["Add to Cart"]
    C --> D["Cart"]
    D --> E["Increase / Decrease"]
    E --> D
    D --> F["Remove Item"]
    D --> G["Checkout"]
```

**Interactive version:** [Open Cart Workflow Viewer](./docs/cart-flow.html)

---

# 📦 Order Workflow

```mermaid
flowchart LR
    A["Cart"] --> B["Create Order"]
    B --> C["Order Placed"]
    C --> D["Order Processing"]
    D --> E["Order Status Updated"]
    E --> F["Delivered"]

    C -.-> X["Cancelled"]
```

**Interactive version:** [Open Order Workflow Viewer](./docs/order-flow.html)

---

# 🧭 API Domain Map

```mermaid
flowchart TB
    API["Food Delivery API"]

    API --> AUTH["Authentication"]
    API --> REST["Restaurants"]
    API --> FOOD["Food Items"]
    API --> CART["Cart"]
    API --> ORDER["Orders"]

    AUTH --> A1["Signup"]
    AUTH --> A2["Login"]

    REST --> R1["Create"]
    REST --> R2["List"]
    REST --> R3["Search"]
    REST --> R4["Get"]
    REST --> R5["Update"]
    REST --> R6["Delete"]

    FOOD --> F1["Create Food Item"]
    FOOD --> F2["List Food Items"]

    CART --> C1["View Cart"]
    CART --> C2["Add Item"]
    CART --> C3["Increase"]
    CART --> C4["Decrease"]
    CART --> C5["Remove"]

    ORDER --> O1["Create Order"]
    ORDER --> O2["List Orders"]
    ORDER --> O3["Get Order"]
    ORDER --> O4["Update Status"]
```

**Interactive version:** [Open API Map Viewer](./docs/api-map.html)

---

# 📡 API Reference

## Authentication

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/auth/signup` | Register a user |
| POST | `/auth/login` | Authenticate a user |

## Restaurants

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/restaurants` | Create restaurant |
| GET | `/restaurants/` | List restaurants |
| GET | `/restaurants/search` | Search restaurants |
| GET | `/restaurants/{id}` | Get restaurant |
| PUT | `/restaurants/{id}` | Update restaurant |
| DELETE | `/restaurants/{id}` | Delete restaurant |
| PATCH | `/restaurants/{id}/image` | Update restaurant image |

## Food Items

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/restaurants/{id}/food-items` | Create food item |
| GET | `/restaurants/{id}/food-items` | List restaurant food items |

## Cart

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/cart/` | Add item to cart |
| GET | `/cart/` | Get cart |
| PATCH | `/cart/{food_item_id}/increase` | Increase quantity |
| PATCH | `/cart/{food_item_id}/decrease` | Decrease quantity |
| DELETE | `/cart/{food_item_id}` | Remove item |

## Orders

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/order/` | Create order |
| GET | `/order/` | List orders |
| GET | `/order/{order_id}` | Get order |
| PATCH | `/order/{order_id}/status_info` | Update order status |

---

# 📁 Project Structure

```text
food_delivary_backend/
│
├── app/
│   ├── routers/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── database/
│   └── main.py
│
├── tests/
│
├── docs/
│   ├── architecture.html
│   ├── request-flow.html
│   ├── auth-flow.html
│   ├── er-diagram.html
│   ├── cart-flow.html
│   ├── order-flow.html
│   └── api-map.html
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# 🚀 Running the Project

## 1. Clone

```bash
git clone https://github.com/SathvikHegade/food_delivary_backend.git
cd food_delivary_backend
```

## 2. Create virtual environment

```bash
python -m venv venv
```

### Windows

```powershell
venv\Scripts\activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure environment variables

Create a `.env` file containing the database and authentication configuration required by the project.

## 5. Start the application

```bash
uvicorn app.main:app --reload
```

---

# 📚 API Documentation

Once the application is running:

- Swagger UI: `/docs`
- ReDoc: `/redoc`

These interfaces make it easy to inspect endpoints and test API requests.

---

# 🐳 Docker

The project also contains Docker configuration for running the backend in a containerized environment.

Typical workflow:

```bash
docker compose up --build
```

---

# 🧪 Testing

Run the project's test suite with:

```bash
pytest
```

---

# 🧠 Backend Request Lifecycle

```text
Client
  │
  ▼
HTTP Request
  │
  ▼
FastAPI Router
  │
  ▼
Validation
  │
  ▼
Business Logic
  │
  ▼
SQLAlchemy ORM
  │
  ▼
PostgreSQL
  │
  ▼
Database Result
  │
  ▼
Pydantic Serialization
  │
  ▼
HTTP Response
  │
  ▼
Client
```

---

# 🎯 Interview Value

This project gives you practical talking points around:

- REST API architecture
- FastAPI routing
- Authentication
- Dependency injection
- ORM and relational databases
- Data validation
- CRUD operations
- Cart and order workflows
- Docker
- API documentation
- Database relationships
- Backend request lifecycle

---

# 🗺️ Interactive Diagram Gallery

| Diagram | Interactive Viewer |
|---|---|
| System Architecture | [Open](./docs/architecture.html) |
| API Request Flow | [Open](./docs/request-flow.html) |
| Authentication | [Open](./docs/auth-flow.html) |
| ER Diagram | [Open](./docs/er-diagram.html) |
| Cart Workflow | [Open](./docs/cart-flow.html) |
| Order Workflow | [Open](./docs/order-flow.html) |
| API Domain Map | [Open](./docs/api-map.html) |

---

## ⚠️ Important

The `README.md` is designed to render directly on GitHub using Mermaid.

The interactive HTML diagrams provide the additional controls that GitHub Markdown itself cannot provide:

**Zoom In · Zoom Out · Pan · Reset · Full Screen**

---

## 👨‍💻 Author

**Sathvik Hegade**

GitHub: `https://github.com/SathvikHegade`
