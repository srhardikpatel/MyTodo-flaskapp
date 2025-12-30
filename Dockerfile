FROM python:3.10-slim

RUN apt update && apt install -y gcc default-libmysqlclient-dev build-essential pkg-config && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install flask_mysqldb
RUN pip install SQLModel

COPY . .

ENTRYPOINT ["python3"]
CMD ["app.py"]
