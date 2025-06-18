FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Install supervisord
RUN apt-get update && apt-get install -y supervisor && apt-get clean

# Create logs directory for supervisord
RUN mkdir -p /var/log/supervisor

# Expose ports
EXPOSE 80 8501

# Start supervisord to run both FastAPI and Streamlit
CMD ["/usr/bin/supervisord", "-c", "/app/supervisord.conf"]
