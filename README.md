# Food Delivery Backend

A RESTful backend API for a food delivery platform built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**. It supports user authentication, restaurant management, menu items, shopping cart, and order processing.

---

## Tech Stack

| Layer          | Technology                          |
|----------------|-------------------------------------|
| Framework      | FastAPI                             |
| ORM            | SQLAlchemy                          |
| Database       | PostgreSQL (via psycopg2-binary)    |
| Authentication | JWT (python-jose) + OAuth2          |
| Password Hash  | bcrypt (passlib)                    |
| Validation     | Pydantic v2                         |
| Server         | Uvicorn                             |

---

## Project Structure

```
food_delivary_backend/
├── .env                          # Environment variables (secrets, DB URL)
├── requirements.txt              # Python dependencies
├── MyVenv/                       # Virtual environment (gitignored)
└── application/
    ├── main.py                   # FastAPI app entry point & router registration
    ├── config.py                 # Loads env vars (DATABASE_URL, SECRET_KEY, etc.)
    ├── database.py               # SQLAlchemy engine, session, and Base
    ├── auth/
    │   ├── JWT_Handler.py        # JWT token creation with expiration
    │   └── oauth2.py             # OAuth2 bearer token validation & user extraction
    ├── models/
    │   ├── users.py              # User model
    │   ├── restaurant.py         # Restaurant model
    │   ├── food_items.py         # FoodItem model
    │   ├── cart.py               # Cart model
    │   ├── order.py              # Order model
    │   └── order_item.py         # OrderItem model
    ├── schemas/
    │   ├── users.py              # User request/response schemas
    │   ├── restaurant.py         # Restaurant request/response schemas
    │   ├── food_items.py         # FoodItem request/response schemas
    │   ├── cart.py               # Cart request/response schemas
    │   └── order.py              # Order request/response schemas & status enum
    └── routes/
        ├── users.py              # Auth routes (signup, login)
        ├── restaurant.py         # Restaurant CRUD + menu management
        ├── cart.py               # Cart operations
        └── order.py              # Order placement, history & status updates
```

---

## Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/SathvikHegade/food_delivary_backend.git
cd food_delivary_backend
```

### 2. Create and activate a virtual environment

```bash
cd food_delivary_backend
python -m venv MyVenv

# Windows
MyVenv\Scripts\activate

# macOS/Linux
source MyVenv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file inside `food_delivary_backend/`:

```env
DATABASE_URL=postgresql://<username>:<password>@<host>:<port>/<database_name>
SECRET_KEY=<your-secret-key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Run the server

```bash
cd application
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`. Interactive docs at `http://127.0.0.1:8000/docs`.

---

## API Endpoints

### Authentication (`/auth`)

| Method   | Endpoint      | Description                | Auth Required |
|----------|---------------|----------------------------|---------------|
| `POST`   | `/auth/signup`| Register a new user        | No            |
| `POST`   | `/auth/login` | Login and receive JWT token| No            |

### Restaurants (`/restaurants`)

| Method   | Endpoint                              | Description                              | Auth Required |
|----------|---------------------------------------|------------------------------------------|---------------|
| `POST`   | `/restaurants`                        | Create a new restaurant                  | Yes           |
| `GET`    | `/restaurants/`                       | Get all restaurants (paginated)          | No            |
| `GET`    | `/restaurants/search`                 | Search by name, rating, or location      | No            |
| `GET`    | `/restaurants/{id}`                   | Get restaurant by ID                     | No            |
| `PUT`    | `/restaurants/{id}`                   | Update restaurant details                | Yes           |
| `DELETE` | `/restaurants/{id}`                   | Delete a restaurant                      | Yes           |
| `PATCH`  | `/restaurants/{id}/image`             | Upload restaurant image                  | Yes           |
| `POST`   | `/restaurants/{id}/food-items`        | Add a menu item                          | Yes           |
| `GET`    | `/restaurants/{id}/food-items`        | Get all menu items for a restaurant      | No            |

### Shopping Cart (`/cart`)

| Method   | Endpoint                          | Description                    | Auth Required |
|----------|-----------------------------------|--------------------------------|---------------|
| `POST`   | `/cart/`                          | Add item to cart               | Yes           |
| `GET`    | `/cart/`                          | View cart with totals          | Yes           |
| `DELETE` | `/cart/{food_item_id}`            | Remove item from cart          | Yes           |
| `PATCH`  | `/cart/{food_item_id}/increase`   | Increase item quantity by 1    | Yes           |
| `PATCH`  | `/cart/{food_item_id}/decrease`   | Decrease item quantity by 1    | Yes           |

### Orders (`/order`)

| Method   | Endpoint                          | Description                    | Auth Required |
|----------|-----------------------------------|--------------------------------|---------------|
| `POST`   | `/order/`                         | Place order from cart          | Yes           |
| `GET`    | `/order/`                         | Get order history              | Yes           |
| `GET`    | `/order/{order_id}`               | Get a single order by ID       | Yes           |
| `PATCH`  | `/order/{order_id}/status_info`   | Update order status            | Yes (owner)   |

**Order Statuses:** `PLACED` -> `CONFIRMED` -> `PREPARING` -> `OUT_FOR_DELIVERY` -> `DELIVERED` | `CANCELLED`

---

## Database Schema

- **User** -- id, username, email, password (hashed)
- **Restaurant** -- id, name, location, rating, owner_id (FK -> User), image_url, cover_image
- **FoodItem** -- id, name, price, description, restaurantID (FK -> Restaurant)
- **Cart** -- id, quantity, user_id (FK -> User), food_item_id (FK -> FoodItem)
- **Order** -- id, user_id (FK -> User), total_amount, status, created_at
- **OrderItem** -- id, order_id (FK -> Order), food_item_id (FK -> FoodItem), quantity, price

---

## License

This project is for educational purposes.
