from fastapi import FastAPI, Depends, HTTPException, Request, Response  # Importa Response
from pydantic import BaseModel
import jwt
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST  # Importa CONTENT_TYPE_LATEST

app = FastAPI()

# Configura métricas
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint'])

# Configuración de JWT
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

# Modelo de usuario
class User(BaseModel):
    username: str
    password: str

# Base de datos falsa
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "password": "secret"
    }
}

# Endpoint de login
@app.post("/login")
def login(user: User):
    if user.username not in fake_users_db or fake_users_db[user.username]["password"] != user.password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = jwt.encode({"sub": user.username}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token}

# Endpoint de métricas
@app.get("/metrics")
def metrics():
    data = generate_latest()  # Genera las métricas en formato de texto plano
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)  # Devuelve la respuesta con el Content-Type correcto

# Middleware para contar solicitudes
@app.middleware("http")
async def count_requests(request: Request, call_next):
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()  # Incrementa el contador
    response = await call_next(request)
    return response

# Ruta raíz
@app.get("/")
def read_root():
    return {"message": "Auth Service is running!"}