# Use official Python slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first (better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose Dash default port
EXPOSE 8050

# Run the app
CMD ["gunicorn", "-b", "0.0.0.0:8050", "app:server"]
