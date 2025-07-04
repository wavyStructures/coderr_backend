# Coderr Backend

The **Coderr Backend** is a REST API built using Django and Django REST Framework (DRF). It powers a platform where customers can connect with business users through structured offers and reviews.

---

## 🔧 Features

- **Authentication**
  - Token-based login and registration (DRF Token Auth)
  - Guest user access for testing (predefined demo accounts)
- **Profile Management**
  - Separate profile types: `customer` and `business`
  - Edit and view profile data
- **Offers**
  - Business users can create offers with tiered levels (basic, standard, premium)
  - Customers can browse offers with filtering and search
- **Orders**
  - Customers can place orders based on offer details
  - Businesses manage orders they receive
- **Reviews**
  - Customers can leave reviews for businesses and specific offers
  - Businesses can view feedback tied to them

---

## 🚀 Quickstart

### Prerequisites

- Python 3.10+
- pip (Python package manager)
- SQLite (default, no setup required)

### Installation Steps

1. **Clone the repository**

   ```bash
   git clone git@github.com/wavyStructures/coderr_backend.git
   cd coderr_backend
   ```

2. **Set up a virtual environment**

   ```bash
   python -m venv env
   source env/bin/activate    # On Linux/Mac
   env\Scripts\activate       # On Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   - Copy `dot_env_template` to `.env`
   - Fill in missing values like `SECRET_KEY`, `EMAIL_*`, etc.
   - Keep SQLite settings as-is:
     ```env
     DATABASE_NAME='db.sqlite3'
     DATABASE_ENGINE='django.db.backends.sqlite3'
     ```

5. **Apply database migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

---

## 👥 Guest Access

Pre-configured demo accounts:

```js
const GUEST_LOGINS = {
  customer: {
    username: "andrey",
    password: "asdasd",
  },
  business: {
    username: "kevin",
    password: "asdasd",
  },
};
```

Use these credentials to test the application with preset roles.

---

## 📘 API Endpoints

### 🔐 Authentication

- `POST /api/login/` – Login and receive token
- `POST /api/registration/` – Register a new user

### 👤 Profiles

- `GET /api/profile/<pk>/` – Retrieve or update user profile
- `GET /api/profiles/business/` – List all business profiles
- `GET /api/profiles/customer/` – List all customer profiles

### 💬 Reviews

- `GET /api/reviews/` – List reviews (filterable)
- `POST /api/reviews/` – Create a review (auth required)
- `GET /api/reviews/<id>/` – Retrieve, update, or delete a review

### 📦 Offers

- `GET /api/offers/` – List all offers
- `POST /api/offers/` – Create new offer (business only)
- `GET /api/offerdetails/<id>/` – Retrieve offer details

### 📄 Orders

- `GET /api/orders/` – View orders
- `POST /api/orders/` – Place a new order (customer only)

---

## 🔐 Environment Variables

Here are the core variables expected in your `.env`:

```env
# URLs
REDIRECT_LOGIN=http://127.0.0.1:5500/index.html
REDIRECT_LANDING=http://127.0.0.1:5500
BACKEND_URL=localhost:8000


# Django settings
SECRET_KEY=your_secret_key
DEBUG = True
ALLOWED_HOSTS=["127.0.0.1", "localhost"]
CSRF_TRUSTED_ORIGINS=["http://localhost:5500", "http://127.0.0.1"]
CORS_ALLOWED_ORIGINS=["http://localhost:5500", "http://127.0.0.1"]

# SQLite by default
DATABASE_ENGINE=django.db.backends.sqlite3
DATABASE_NAME=db.sqlite3
```

---

## 🛠 Deployment Notes

> For development, SQLite and `runserver` are sufficient. For production:

1. Set `DEBUG=False` in `.env`
2. Configure a proper WSGI server (e.g., via `mod_wsgi` or `uWSGI`)
3. Serve static files:
   ```bash
   python manage.py collectstatic
   ```
4. Set up a reverse proxy like **Nginx** if deploying on Linux

---

## 🧪 Contribution

1. Fork this repository
2. Create your feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add: Your feature description"
   ```
4. Push and open a pull request:
   ```bash
   git push origin feature/your-feature-name
   ```

---

## 📄 License

Licensed under the MIT License.
