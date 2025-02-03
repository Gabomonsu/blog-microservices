# Blog Microservices

Este proyecto es un sistema de blog basado en microservicios, construido con FastAPI, Docker, Prometheus y Grafana.

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/blog-microservices.git
   cd blog-microservices

2. Levanta los contenedores:

   docker-compose up --build

3. Accede a los servicios:
  API Gateway: http://localhost:8000
  Prometheus: http://localhost:9090
  Grafana: http://localhost:3000


requirements.txt:
Lista las dependencias de Python para cada servicio.
docker-compose.yml:
Define los servicios, redes y volúmenes del proyecto.
Carpetas de cada servicio:
auth-service/, post-service/, comment-service/, api-gateway/, monitoring/.
