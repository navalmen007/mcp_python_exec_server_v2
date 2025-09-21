FROM python:3.11-alpine

# Install system dependencies required for pandas and numpy
RUN apk add --no-cache \
    build-base \
    libffi-dev \
    musl-dev \
    gcc \
    gfortran \
    python3-dev \
    py3-numpy \
    openblas-dev

WORKDIR /app

# Copy project files into the container
COPY . .

# Upgrade pip and install project dependencies (pandas included via pyproject.toml)
RUN pip install --upgrade pip \
    && pip install .

# Run the MCP server
CMD ["python", "FastMCP_server_python_exec.py"]
