## FastAPI + PostgreSQL + Redis + NGINX (Dockerized)

### Architecture
```
+-------------+     +-------------+     +-----------+
|  NGINX      | --> |  FastAPI    | --> |  PostgreSQL
|  (Reverse   |     |  Backend    | --> |  Redis     |
|  Proxy)     |     |  API        |     |  Cache     |
+-------------+     +-------------+     +-----------+
```

### Usage
```bash
docker-compose up --build
```

### Check Logs
Use docker-compose logs or check specific containers:

```bash
docker-compose logs nginx
docker-compose logs fastapi
docker-compose logs db
docker-compose logs redis
```
Look for:

502 Bad Gateway from NGINX? → FastAPI may be down.

Connection errors? → Maybe wrong env vars or service names.

### Interactive Verification
Use the Docker CLI:
```bash
docker ps
docker network inspect fastapi_postgres_redis_nginx_backend
docker volume inspect fastapi_postgres_redis_nginx_postgres_data
```

### Check NGINX Reverse Proxy
Test: Visit http://localhost in your browser or use:
```bash
curl -i http://localhost
```
Expected Output:
```http
HTTP/1.1 200 OK
...
{"message":"FastAPI with PostgreSQL, Redis, and NGINX is working!"}
```
If this works, NGINX is successfully reverse-proxying to FastAPI.

### Check PostgreSQL Connection
Right now, the app doesn’t yet query the database, but you can test the connection by:

Adding a dummy table and querying it via FastAPI
```bash
curl -X POST "http://localhost/items/testitem"
curl "http://localhost/items"
```

Or testing connection inside the container:
```bash
docker exec -it fastapi_app python
```
Then in Python shell:
```python
from sqlalchemy import create_engine, text

# Create engine with PostgreSQL URL
engine = create_engine("postgresql://postgres:postgres@db:5432/postgres")

# Connect and execute a test query
with engine.connect() as conn:
    result = conn.execute(text("SELECT 1")).scalar()
    print(result)
```
Expected: 1

### Check Redis Caching
Test POST (set cache):
```bash
curl -X POST "http://localhost/cache/testkey?value=testvalue"
```

Test GET (retrieve from cache):
```bash
curl "http://localhost/cache/testkey"
```

Expected Output:
```json
{"key":"testkey","value":"testvalue"}
```
If you receive that, it confirms Redis is connected and caching works.


### Health Check
```bash
curl http://localhost/health
```
Should return a JSON like:
```json
{
  "postgresql": "ok",
  "redis": "ok"
}
```

### Security Scan
To scan your Docker images:
```bash
trivy image fastapi_app
# or using Docker Scout
docker scout quickview fastapi_app
```

Make sure to install [Trivy](https://github.com/aquasecurity/trivy) or [Docker Scout](https://docs.docker.com/scout/).

## # Attached trivy scan results in json format #

### Recommendation
If you want to stay current and minimize image vulnerabilities, update your image tags to:

```yaml
db:
  image: postgres:16-alpine

redis:
  image: redis:7.2-alpine

nginx:
  image: nginx:alpine  # Still fine

# In app/Dockerfile
FROM python:3.12-alpine AS builder
...
FROM python:3.12-alpine
```

### Features
- Lightweight alpine-based images
- Multi-stage Docker build for optimized image size
- Redis caching for performance
- PostgreSQL for persistent storage
- NGINX reverse proxy
- Security scanning ready with Trivy or Docker Scout
