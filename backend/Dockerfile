FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create uploads directory for PDF files
RUN mkdir -p uploads

# Expose port
EXPOSE $PORT

# Run the application
CMD gunicorn --bind 0.0.0.0:$PORT app:app
