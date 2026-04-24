FROM python:3.13-slim

WORKDIR /app

RUN python3 -m pip install --upgrade pip

RUN apt-get update && \
    apt-get install -y \
    pkg-config \
    default-libmysqlclient-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8080
EXPOSE 3298

CMD ["python3", "main.py"]