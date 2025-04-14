FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
COPY src/bot.py .
COPY .creds .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "bot.py"]