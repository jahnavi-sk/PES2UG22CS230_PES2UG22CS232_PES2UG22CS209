FROM python:3.10-slim

# Install Redis
RUN apt-get update && apt-get install -y redis-server

# Set up working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY templates templates/

# Create startup script
RUN echo '#!/bin/bash\nredis-server --daemonize yes\npython app.py' > /app/start.sh
RUN chmod +x /app/start.sh

# Expose port
EXPOSE 5000

# Run the application
CMD ["/app/start.sh"]