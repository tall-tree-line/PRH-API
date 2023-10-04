FROM python:3.11.3-slim

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY .env /app/
COPY prh /app/prh
COPY bulk.py /app/
COPY single.py /app/
COPY create_tables.py /app/



CMD ["python", "bulk.py"]
