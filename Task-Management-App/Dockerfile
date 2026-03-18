# Use slim Python image
FROM python:3.11-slim as builder

WORKDIR /app

# Set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt

# Copy project
COPY . .

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY scripts/start.sh /app/scripts/start.sh
RUN chmod +x /app/scripts/start.sh
COPY . .

EXPOSE 8000

# Run migrations and start server
CMD ["/app/scripts/start.sh"]
