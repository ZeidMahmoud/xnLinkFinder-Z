# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    wget \
    curl \
    poppler-utils \
    ocrmypdf \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install chromium
RUN playwright install-deps chromium

# Copy application code
COPY . .

# Install xnLinkFinder-Z
RUN pip install -e .

# Create directories for config and output
RUN mkdir -p /root/.config/xnLinkFinder /output

# Copy default config
COPY config.yml /root/.config/xnLinkFinder/

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Default command
ENTRYPOINT ["xnLinkFinder"]
CMD ["--help"]
