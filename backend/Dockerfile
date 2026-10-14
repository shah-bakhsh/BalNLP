FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 HF_HOME=/cache/huggingface BALNLP_DEVICE=cpu
WORKDIR /app
RUN useradd --create-home --uid 10001 balnlp && mkdir -p /cache/huggingface && chown -R balnlp:balnlp /cache
COPY pyproject.toml README.md LICENSE NOTICE ./
COPY balnlp ./balnlp
COPY backend ./backend
RUN pip install --no-cache-dir torch==2.14.0 --index-url https://download.pytorch.org/whl/cpu && pip install --no-cache-dir '.[api,inference]'
USER balnlp
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s CMD python -c "import urllib.request,os; urllib.request.urlopen('http://127.0.0.1:'+os.environ.get('PORT','8000')+'/api/v1/health',timeout=3)"
CMD ["sh", "-c", "exec uvicorn backend.app.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1 --no-access-log --no-proxy-headers"]
