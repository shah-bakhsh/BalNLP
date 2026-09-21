FROM node:24-bookworm-slim AS website
WORKDIR /build
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
ENV BALNLP_STATIC_EXPORT=1 NEXT_PUBLIC_API_URL=/api/v1 NEXT_TELEMETRY_DISABLED=1
RUN npm run build

FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 HF_HOME=/home/user/.cache/huggingface BALNLP_DEVICE=cpu BALNLP_CPU_THREADS=2 BALNLP_MEMORY_MODE=low BALNLP_WARMUP=false BALNLP_STATIC_DIR=/app/static PORT=7860
RUN useradd --create-home --uid 1000 user
COPY pyproject.toml README.md LICENSE ./
COPY balnlp ./balnlp
COPY backend ./backend
RUN pip install --no-cache-dir torch==2.14.0 --index-url https://download.pytorch.org/whl/cpu && pip install --no-cache-dir '.[api,inference]'
COPY --from=website /build/out /app/static
USER user
EXPOSE 7860
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:7860/api/v1/health',timeout=3)"
CMD ["sh", "-c", "exec uvicorn backend.app.main:app --host 0.0.0.0 --port ${PORT:-7860} --workers 1 --no-access-log --no-proxy-headers"]
