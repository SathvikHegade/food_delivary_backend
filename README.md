# 🍔 Food Delivery Backend

A production-oriented REST API backend for a food delivery platform built with **FastAPI, PostgreSQL, SQLAlchemy and Redis**.

The project has evolved from a basic REST API into a backend with **JWT authentication, authorisation, Redis caching, cache-stampede protection, distributed locking, sliding-window rate limiting, IP blocking, security email alerts, Dockerisation and automated testing**.

---

## 🚀 Features

### 👤 Authentication & Security
- User registration and login
- JWT-based authentication
- bcrypt password hashing
- Authentication and authorisation
- Restaurant ownership validation
- Sliding-window failed-login rate limiting
- Temporary IP blocking
- Security email alerts

### 🍽️ Core Features
- Restaurant CRUD and search
- Food-item management
- Cart management
- Order management
- Order history and status updates
- Verified-purchase restaurant reviews
- Automatic restaurant rating updates

### ⚡ Redis & Performance
- Restaurant response caching
- TTL-based expiration
- Cache invalidation
- Cache-stampede protection
- Distributed Redis locking
- Atomic Redis Lua operations

### 🐳 Infrastructure & Testing
- Docker + Docker Compose
- PostgreSQL container
- Redis container
- Pytest authentication tests
- Swagger / OpenAPI documentation

---

# 🏗️ System Architecture

```mermaid
flowchart TD
    Client["Client / Frontend / Swagger"]
    API["FastAPI Application"]

    Client --> API

    API --> Auth["Authentication & JWT"]
    API --> Restaurant["Restaurant Management"]
    API --> Food["Food Items"]
    API --> Cart["Cart Management"]
    API --> Order["Order Management"]
    API --> Review["Review System"]

    Auth --> DB[("PostgreSQL")]
    Restaurant --> DB
    Food --> DB
    Cart --> DB
    Order --> DB
    Review --> DB

    API --> Redis["Redis"]

    Redis --> Cache["Caching"]
    Redis --> Rate["Sliding Window Rate Limiter"]
    Redis --> Lock["Distributed Lock"]
    Redis --> Block["IP Blocking"]

    Auth --> Email["Gmail SMTP"]
    Block --> Email

    API --> Docker["Docker"]
```

---

# 📈 Backend Development Evolution

```mermaid
flowchart LR
    A["Basic REST API"]
    --> B["PostgreSQL + SQLAlchemy"]
    --> C["JWT Authentication"]
    --> D["Authorisation & Ownership"]
    --> E["Cart & Order System"]
    --> F["Review System"]
    --> G["Redis Integration"]
    --> H["Redis Caching"]
    --> I["Cache Invalidation"]
    --> J["Cache Stampede Protection"]
    --> K["Distributed Redis Lock"]
    --> L["Sliding Window Rate Limiter"]
    --> M["IP Blocking"]
    --> N["Security Email Alerts"]
    --> O["Dockerisation"]
    --> P["Automated Testing"]
```

---

# 🔐 Login Security

```mermaid
flowchart TD
    A["Login Request"] --> B["Rate Limit Dependency"]

    B --> C{"IP Blocked?"}
    C -->|Yes| D["429 Too Many Requests"]
    C -->|No| E["Find User"]

    E --> F{"User Exists?"}
    F -->|No| G["Record Failed Attempt"]
    F -->|Yes| H["Verify Password"]

    G --> I["401 Unauthorized"]

    H --> J{"Password Correct?"}
    J -->|Yes| K["Generate JWT"]
    K --> L["200 OK"]

    J -->|No| M["Record Failed Attempt"]
    M --> N{"5th Failure?"}

    N -->|No| O["401 Unauthorized"]
    N -->|Yes| P["Create Redis IP Block"]

    P --> Q["Send Security Email"]
    Q --> O
```

### Login behaviour

```text
Failed attempt #1 → 401
Failed attempt #2 → 401
Failed attempt #3 → 401
Failed attempt #4 → 401
Failed attempt #5 → 401 + IP Block + Security Email
Next attempt       → 429
```

---

# ⚡ Redis Caching

```mermaid
flowchart TD
    A["GET Restaurant"] --> B{"Redis Cache Hit?"}

    B -->|Yes| C["Return Cached Data"]
    B -->|No| D{"Acquire Distributed Lock"}

    D -->|Lock Unavailable| E["Wait and Retry Redis"]
    E --> B

    D -->|Lock Acquired| F["Query PostgreSQL"]
    F --> G["Store Result in Redis"]
    G --> H["Release Redis Lock"]
    H --> I["Return Restaurant"]
```

PostgreSQL remains the **source of truth**, while Redis acts as a fast cache and coordination layer.

---

# 🔒 Cache Stampede Protection

```mermaid
flowchart TD
    A["Multiple Requests"] --> B["Redis Cache"]

    B --> C{"Cache Hit?"}
    C -->|Yes| D["Return Cached Data"]
    C -->|No| E["Try Distributed Lock"]

    E --> F{"Lock Acquired?"}
    F -->|Yes| G["Query PostgreSQL"]
    G --> H["Update Redis"]
    H --> I["Release Lock"]

    F -->|No| J["Wait / Retry Redis"]
    J --> B

    I --> D
```

Redis distributed locks prevent many concurrent requests from rebuilding the same expired cache entry.

Implementation concepts:
- `SET NX`
- Lock TTL
- Unique lock tokens
- Atomic Lua compare-and-delete

---

# 🚦 Rate Limiting

```mermaid
flowchart TD
    A["Login Request"] --> B["Extract Client IP"]
    B --> C["Redis Sorted Set"]

    C --> D["Remove Expired Attempts"]
    D --> E["Add Current Attempt"]
    E --> F["Count Attempts"]

    F --> G{"Count >= Limit?"}

    G -->|No| H["Allow Request"]
    G -->|Yes| I["Create Temporary IP Block"]

    I --> J["Future Requests → 429"]
```

The rate limiter uses a **Redis Sorted Set** and an **atomic Lua script** to perform the sliding-window operation safely under concurrent requests.

---

# 📧 Security Email Alerts

```mermaid
flowchart TD
    A["Failed Login"] --> B["Redis Rate Limiter"]
    B --> C{"Threshold Reached?"}

    C -->|No| D["Continue"]
    C -->|Yes| E["Create IP Block"]

    E --> F["Security Alert"]
    F --> G["Gmail SMTP"]
    G --> H["Account Owner"]
```

The email is a **notification**, while Redis rate limiting and IP blocking provide the actual protection.

---

# 🗄️ Database Architecture

```mermaid
erDiagram
    USER ||--o{ RESTAURANT : owns
    USER ||--o{ CART : has
    USER ||--o{ ORDER : places
    USER ||--o{ REVIEW : writes

    RESTAURANT ||--o{ FOOD_ITEM : contains
    RESTAURANT ||--o{ REVIEW : receives

    CART ||--o{ CART_ITEM : contains
    FOOD_ITEM ||--o{ CART_ITEM : added_to

    ORDER ||--o{ ORDER_ITEM : contains
    FOOD_ITEM ||--o{ ORDER_ITEM : ordered_as

    USER {
        int id PK
        string username
        string email
        string password
    }

    RESTAURANT {
        int id PK
        string name
        string location
        float rating
        int owner_id FK
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

    CART_ITEM {
        int id PK
        int cart_id FK
        int food_item_id FK
        int quantity
    }

    ORDER {
        int id PK
        int user_id FK
        float total_amount
        string status
    }

    ORDER_ITEM {
        int id PK
        int order_id FK
        int food_item_id FK
        int quantity
    }

    REVIEW {
        int id PK
        int user_id FK
        int restaurant_id FK
        float rating
        string comment
    }
```

---

# ⭐ Review System

```mermaid
flowchart TD
    A["Authenticated User"] --> B["Submit Review"]
    B --> C{"Verified Purchase?"}

    C -->|No| D["Reject Review"]
    C -->|Yes| E["Create Review"]

    E --> F["Calculate Average Rating"]
    F --> G["Update Restaurant Rating"]
    G --> H["Invalidate Redis Cache"]
```

---

# 📦 Order Flow

```mermaid
flowchart TD
    A["User"] --> B["Cart"]
    B --> C["Place Order"]
    C --> D["Create Order"]
    D --> E["Order Placed"]
    E --> F["Order Processing"]
    F --> G["Status Updates"]
    G --> H["Delivered"]

    E -.-> I["Cancelled"]
```

---

# 🔄 Request Lifecycle

```mermaid
flowchart TD
    A["Client"] --> B["HTTP Request"]
    B --> C["FastAPI"]
    C --> D["Dependency Injection"]
    D --> E["Request Validation"]
    E --> F["Router"]
    F --> G["Business Logic"]

    G --> H["SQLAlchemy ORM"]
    H --> I[("PostgreSQL")]

    G --> J["Redis"]

    G --> K["Response Schema"]
    K --> L["HTTP Response"]
    L --> A
```

---

# 🐳 Docker Architecture

```mermaid
flowchart LR
    Web["FastAPI Container"]
    DB[("PostgreSQL Container")]
    Redis[("Redis Container")]

    Web --> DB
    Web --> Redis
```

Start the complete application with:

```bash
docker compose up --build
```

---

# 🧱 Project Structure

```text
food_delivary_backend/
│
├── application/
│   ├── auth/
│   │   ├── JWT_Handler.py
│   │   └── rate_limiter.py
│   │
│   ├── models/
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   │   └── email_service.py
│   │
│   ├── database.py
│   ├── redis_client.py
│   ├── logger.py
│   └── main.py
│
├── tests/
│   └── test_auth.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .gitignore
└── README.md
```

---

# 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend |
| FastAPI | REST API |
| PostgreSQL | Database |
| SQLAlchemy | ORM |
| Pydantic | Validation |
| Redis | Cache, locking & rate limiting |
| JWT | Authentication |
| bcrypt | Password hashing |
| Docker | Containerisation |
| Docker Compose | Orchestration |
| Pytest | Testing |
| SMTP / Gmail | Security alerts |
| Swagger / OpenAPI | API documentation |

---

# 📡 API Overview

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/signup` | Register user |
| POST | `/auth/login` | Login |

### Restaurants

| Method | Endpoint | Description |
|---|---|---|
| POST | `/restaurants` | Create restaurant |
| GET | `/restaurants/` | List restaurants |
| GET | `/restaurants/{id}` | Get restaurant |
| PUT | `/restaurants/{id}` | Update restaurant |
| DELETE | `/restaurants/{id}` | Delete restaurant |

### Food Items

| Method | Endpoint | Description |
|---|---|---|
| POST | `/restaurants/{id}/food-items` | Add food item |
| GET | `/restaurants/{id}/food-items` | Get food items |

### Cart

| Method | Endpoint | Description |
|---|---|---|
| GET | `/cart/` | Get cart |
| POST | `/cart/` | Add item |
| PATCH | `/cart/{id}/increase` | Increase quantity |
| PATCH | `/cart/{id}/decrease` | Decrease quantity |
| DELETE | `/cart/{id}` | Remove item |

### Orders

| Method | Endpoint | Description |
|---|---|---|
| POST | `/order/` | Place order |
| GET | `/order/` | Order history |
| GET | `/order/{id}` | Order details |

### Reviews

| Method | Endpoint | Description |
|---|---|---|
| POST | `/restaurants/{id}/reviews` | Add review |

For complete interactive API documentation, use Swagger.

---

# 🚀 Getting Started

### 1. Clone

```bash
git clone https://github.com/SathvikHegade/food_delivary_backend.git
cd food_delivary_backend
```

### 2. Configure environment variables

Create a `.env` file:

```env
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=food_delivery

DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USERNAME=your_email
EMAIL_PASSWORD=your_gmail_app_password
```

> ⚠️ Never commit real credentials or `.env` to GitHub.

### 3. Start

```bash
docker compose up --build
```

Application:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

ReDoc:

```text
http://localhost:8000/redoc
```

---

# 🧪 Testing

Run:

```bash
pytest -v
```

PowerShell, if required:

```powershell
$env:PYTHONPATH="application"
pytest -v
```

---

# 🔐 Security Highlights

- JWT authentication
- bcrypt password hashing
- Dependency-based authentication
- Ownership-based authorisation
- Redis sliding-window rate limiting
- Atomic Redis Lua operations
- Temporary IP blocking
- Distributed Redis locks
- Cache-stampede protection
- Security email notifications
- Environment-based secrets
- Verified-purchase reviews

---

# 📚 Backend Concepts Demonstrated

```mermaid
flowchart TD
    A["REST API Design"]
    --> B["FastAPI"]
    --> C["Dependency Injection"]
    --> D["Authentication"]
    --> E["Authorisation"]
    --> F["PostgreSQL + SQLAlchemy"]
    --> G["Redis"]
    --> H["Caching"]
    --> I["Cache Invalidation"]
    --> J["Cache Stampede Protection"]
    --> K["Distributed Locking"]
    --> L["Rate Limiting"]
    --> M["IP Blocking"]
    --> N["Security Monitoring"]
    --> O["Docker"]
    --> P["Automated Testing"]
```

---

# 👨‍💻 Author

**T S Sathvik Hegade**

Computer Science Engineering Student

[GitHub](https://github.com/SathvikHegade)

---

## 📄 License

This project is licensed under the MIT License.
