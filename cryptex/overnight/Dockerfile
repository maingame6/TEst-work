FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 CRYPTEX_BIND=0.0.0.0 CRYPTEX_DB=/data/cryptex.sqlite3
WORKDIR /app
COPY engine.py overnight.html ./
USER 65534
EXPOSE 8765
CMD ["python", "-u", "engine.py", "serve"]