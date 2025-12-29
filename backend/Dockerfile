# Build stage
FROM python:3.11-alpine AS builder

WORKDIR /app

# Install build dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-dev \
    libffi-dev

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Runtime stage
FROM python:3.11-alpine

WORKDIR /app

# Install only runtime dependencies
RUN apk add --no-cache \
    libpq \
    libffi \
    postgresql-client

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local

# Copy only necessary application code
COPY app ./app
COPY alembic.ini ./

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
