
# Stage 1
# Build the Vite Frontend

FROM node:22-slim AS frontend-builder

WORKDIR /frontend

COPY UI/pdfExtractor_UI/package*.json ./

RUN npm ci

COPY UI/pdfExtractor_UI ./

RUN npm run build 

# Stage 2
# Build the FASTAPI Runtime

FROM python:3.12-slim 

WORKDIR /app/Backend 

RUN apt-get update && \
    apt-get install -y \
        tesseract-ocr \
        libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv    

COPY Backend/pyproject.toml Backend/uv.lock ./

RUN uv sync --frozen --no-dev 

COPY Backend ./

COPY --from=frontend-builder /frontend/dist /app/Backend/static_dist

CMD ["sh", "-c", "uv run uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-10000}"]

