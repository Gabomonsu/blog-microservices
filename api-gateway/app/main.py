from fastapi import FastAPI
import requests
from prometheus_client import make_asgi_app, Counter, generate_latest

app = FastAPI()

# Configura métricas
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint'])

# URLs de los servicios
AUTH_SERVICE_URL = "http://auth-service:8000"
POST_SERVICE_URL = "http://post-service:8000"
COMMENT_SERVICE_URL = "http://comment-service:8000"

# Endpoint de login
@app.post("/login")
def login(user: dict):
    response = requests.post(f"{AUTH_SERVICE_URL}/login", json=user)
    return response.json()

# Endpoint para crear publicaciones
@app.post("/posts")
def create_post(post: dict):
    response = requests.post(f"{POST_SERVICE_URL}/posts", json=post)
    return response.json()

# Endpoint para obtener publicaciones
@app.get("/posts")
def get_posts():
    response = requests.get(f"{POST_SERVICE_URL}/posts")
    return response.json()

# Endpoint para crear comentarios
@app.post("/comments")
def create_comment(comment: dict):
    response = requests.post(f"{COMMENT_SERVICE_URL}/comments", json=comment)
    return response.json()

# Endpoint para obtener comentarios
@app.get("/comments")
def get_comments():
    response = requests.get(f"{COMMENT_SERVICE_URL}/comments")
    return response.json()

# Endpoint de métricas
@app.get("/metrics")
def metrics():
    return generate_latest()

# Middleware para contar solicitudes
@app.middleware("http")
async def count_requests(request, call_next):
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    response = await call_next(request)
    return response

# Ruta raíz
@app.get("/")
def read_root():
    return {"message": "API Gateway is running!"}