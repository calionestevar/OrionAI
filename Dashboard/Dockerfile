FROM python:3.11-slim

WORKDIR /app

# Copy dashboard files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ellie.py .
COPY templates/ templates/

# Copy OrionAI Python module
COPY ../Python/orionai.py /app/orionai.py

# Config will be mounted as volume
VOLUME /app/Config

EXPOSE 5000

CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "ellie:app", "--bind", "0.0.0.0:5000"]
