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

### Security Scan
To scan your Docker images:
```bash
trivy image fastapi_app
# or using Docker Scout
docker scout quickview fastapi_app
```

Make sure to install [Trivy](https://github.com/aquasecurity/trivy) or [Docker Scout](https://docs.docker.com/scout/).

### Features
- Lightweight alpine-based images
- Multi-stage Docker build for optimized image size
- Redis caching for performance
- PostgreSQL for persistent storage
- NGINX reverse proxy
- Security scanning ready with Trivy or Docker Scout
