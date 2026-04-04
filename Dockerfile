FROM python:3.12-slim

WORKDIR /app

RUN python3 -m pip install --upgrade pip

# Installiere Systemabhängigkeiten für mysqlclient
RUN apt-get update && \
    apt-get install -y \
    pkg-config \
    default-libmysqlclient-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Kopiere requirements.txt und installiere Python-Pakete
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den Rest des Codes
COPY . .

ENV PORT=8080
EXPOSE 3298

CMD ["python3", "system_setup.py", "create_db", "&" ,"python3", "main.py"]