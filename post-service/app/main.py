from fastapi import FastAPI, Request, Response  # Importa Response
from pydantic import BaseModel
from typing import List
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST  # Importa CONTENT_TYPE_LATEST

app = FastAPI()

# Configura métricas
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint'])

# Modelo de publicación
class Post(BaseModel):
    id: int
    title: str
    content: str

# Base de datos falsa
fake_posts_db = []

# Endpoint para crear publicaciones
@app.post("/posts", response_model=Post)
def create_post(post: Post):
    fake_posts_db.append(post)
    return post

# Endpoint para obtener publicaciones
@app.get("/posts", response_model=List[Post])
def get_posts():
    return fake_posts_db

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
    return {"message": "Post Service is running!"}