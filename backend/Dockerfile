#FROM python:3.8-alpine
#
#WORKDIR /backend
#
## Установка системных зависимостей
#RUN apk update && apk add --no-cache \
#    gcc \
#    musl-dev \
#    linux-headers \
#    && pip install --upgrade pip \
#    && rm -rf /var/cache/apk/*
#
#COPY requirements.txt .
#
## Обновление pip и установка зависимостей
#RUN pip install --no-cache-dir --upgrade pip && \
#    pip install --no-cache-dir -r requirements.txt
#
#COPY . .
#
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]


# === Этап сборки ===
FROM python:3.8-alpine AS build

WORKDIR /backend

RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    linux-headers \
    python3-dev

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install cython

COPY . .

# Компиляция только math_service.py в .so
RUN cython -3 app/services/math_service.py && \
    gcc -shared -fPIC $(python3-config --includes) \
        app/services/math_service.c \
        -o app/services/math_service.so && \
    rm app/services/math_service.py app/services/math_service.c

# === Финальный образ ===
FROM python:3.8-alpine

WORKDIR /backend

# Устанавливаем runtime-зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем скомпилированные файлы
COPY --from=build /backend /backend

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
