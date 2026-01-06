FROM python:3.15-rc-alpine3.22

RUN apt update && apt install -y gcc default-libmysqlclient-dev build-essential pkg-config && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install flask_mysqldb
RUN pip install SQLModel

COPY . .

ENTRYPOINT ["python3"]
CMD ["app.py"]
