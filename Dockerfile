FROM python:3.10-slim

# Set workdir
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY backend/ backend/
COPY templates/ templates/
COPY static/ static/
COPY .env .env

# Expose Flask port
EXPOSE 5000

# Run Flask
CMD ["python", "backend/app.py"]
