# Use Python 3.13 slim image as base
FROM python:3.13-slim

# Install uv for fast Python package management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# Set working directory to the Python project
WORKDIR /app

# Copy the Python project files
COPY spyglass-deployment-action/ .

# Install dependencies using uv
RUN uv sync --frozen

# Set the entrypoint to run the main script from the app directory
ENTRYPOINT ["sh", "-c", "cd /app && uv run python main.py"]
