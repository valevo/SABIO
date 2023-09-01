FROM python:3.10

# Create app user
RUN useradd -m -U appuser

# Install server in /app
WORKDIR /app

# Install python dependencies in /app
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy all other files
COPY . .

# Environment variables
ENV LIMIT_REQUIRES_LINE=8190
ENV LOG_LEVEL=critical
ENV PORT=8080
ENV SCRIPT_NAME=/api/v1/
ENV TIMEOUT=600
ENV WORKERS=2

# Run as appuser
USER appuser

# Use start script to run the gunicorn server
CMD ["./start.sh"]
