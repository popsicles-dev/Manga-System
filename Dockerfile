# Use an official Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Optional: install build tools if needed by some packages
RUN apt-get update && apt-get install -y build-essential

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app code into the container
COPY ./model_files /app/app/model


# Expose FastAPI and Streamlit ports
EXPOSE 8000
EXPOSE 8501

# Run FastAPI and Streamlit in parallel
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port 8000 & streamlit run streamlit_app.py --server.port 8501"]
