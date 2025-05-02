````markdown
# 🔗 URL Shortener API (FastAPI)

A simple and lightweight URL shortener API built using FastAPI and SQLite.

---

## 🚀 Features

- Shortens valid long URLs
- Redirects to original URLs
- Stores data in SQLite
- Environment variable support with `.env`

---

## 🛠️ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/your-username/url-short-api.git
cd url-short-api
````

### 2. Create a virtual environment and activate it

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install fastapi uvicorn pydantic validators python-dotenv requests
```

### 4. Create a `.env` file in the root directory

```env
BASE_URL=http://localhost:8000/
DB_PATH=urlshortner.db
```

### 5. Run the server

```bash
uvicorn app:app --reload
```

---

## 📦 API Endpoints

### ➕ POST `/shorten`

Shortens a long URL.

**Request Body:**

```json
{
  "url": "https://example.com"
}
```

**Response:**

```json
{
  "shorturl": "http://localhost:8000/XyZ123"
}
```

---

### 🔁 GET `/{code}`

Redirects to the original long URL using the unique code.

**Example:**

```
GET http://localhost:8000/XyZ123
```

Will redirect to:

```
https://example.com
```

---

## 🗃️ Database

* SQLite DB path is set via `DB_PATH` in `.env`
* Table: `URLSHORTNER`

  * `longurl`: Original URL
  * `shorturl`: Shortened URL
  * `code`: Unique 6-character code (primary key)

---

## ✅ To Do

* Add analytics
* Add URL expiry
* Add simple frontend
