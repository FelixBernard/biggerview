FROM python:3.12-alpine

WORKDIR /app

RUN python3 -m pip install --upgrade pip

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8080

EXPOSE 8080

CMD ["python3", "main.py"]