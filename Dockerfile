FROM python:3.11-slim

WORKDIR /app

# Dependencies
COPY requirements-webhook.txt .
RUN pip install --no-cache-dir -r requirements-webhook.txt

# App code — only what USSD needs
COPY webhook_ussd.py .
COPY services/ussd_service.py ./services/
COPY services/__init__.py ./services/ 2>/dev/null || touch services/__init__.py

ENV PORT=8080
EXPOSE 8080

CMD ["sh", "-c", "uvicorn webhook_ussd:app --host 0.0.0.0 --port ${PORT} --workers 2"]
