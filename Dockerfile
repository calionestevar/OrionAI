# Dockerfile for OrionAI Python Service
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY Python/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy OrionAI module and configuration
COPY Python/orionai.py .
COPY Config/ ./Config/

# Set environment variables for integrations
ENV SLACK_WEBHOOK_URL=""
ENV GITHUB_API_TOKEN=""
ENV JIRA_API_TOKEN=""
ENV JIRA_URL=""

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import orionai; print('OK')" || exit 1

# Run example service (replace with your actual service)
CMD ["python", "-c", "from orionai import OrionAI; orion = OrionAI(); print('OrionAI service ready')"]
