FROM python:3.12-alpine

WORKDIR /backend

# Установка системных зависимостей
RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    linux-headers \
    && pip install --upgrade pip \
    && rm -rf /var/cache/apk/*

COPY requirements.txt .

# Обновление pip и установка зависимостей
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]