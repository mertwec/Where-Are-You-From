# 🌍 Where Are You From


Mini service that determines a person's probable country of origin based on their name using external APIs and stores aggregated data in a local database. Suitable for use by researchers, marketers, and analysts.


## 🔧 Setup and run

### 1. Clone repository

```bash
git clone https://github.com/mertwec/Where-Are-You-From.git
cd Where-Are-You-From
```

###  2. 🌱 add file `.env` with parameters:
for example see `.env_example`
```
SECRET_KEY = "your_secret key"

DB_NAME = "db_name"
DB_USER = "user_name"
DB_PASSWORD = "password_db"

DEBUG = False
```
For generate SECRET_KEY, use command:
```bash
python3 ./utils/gen_secret_key.py
```

### 3. Run in Docker

```bash
docker compose up --build
```

### 4. The application will be available at:
📍 http://localhost:8000

---

### 📋 Примеры API

|api|description|
|---|---|
|`GET /names/?name=johnson`|Returns a list of countries and origin probabilities for the specified name. If the data is already in the database and is not older than a day, the cache is returned. Otherwise, a request is made to Nationalize and REST Countries.|
|`GET /popular-names/?country=US` |  Returns the top 5 most common names associated with a country. |

### 🧪 Tests
The tests use a test database

For run unit-tests:
run docker with database postgres or create database "db_base_test"!!!

`pytest --cov=.`

### 🔐 Authentication
JWT authentication is used to access protected endpoints.


### 📚 Документация API
Swagger :
🔗 http://localhost:8000/docs
ReDoc:
🔗 http://localhost:8000/redoc

