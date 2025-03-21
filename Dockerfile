FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    cron \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p output logs

# Make scripts executable
RUN chmod +x src/run.sh src/run_scheduler.sh src/setup.sh

# Set up cron jobs
RUN echo "0 8 * * * cd /app && python src/main.py --type daily >> /app/logs/cron.log 2>&1" > /etc/cron.d/google-trends-tracker
RUN echo "0 9 * * 1 cd /app && python src/main.py --type weekly >> /app/logs/cron.log 2>&1" >> /etc/cron.d/google-trends-tracker
RUN echo "0 10 1 * * cd /app && python src/main.py --type monthly >> /app/logs/cron.log 2>&1" >> /etc/cron.d/google-trends-tracker
RUN chmod 0644 /etc/cron.d/google-trends-tracker

# Create entrypoint script
RUN echo '#!/bin/bash\n\
cron\n\
# Run the scheduler in foreground\npython src/scheduler.py' > /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Run the entrypoint script
CMD ["/app/entrypoint.sh"]
