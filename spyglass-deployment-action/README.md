# Spyglass Deployment Action - Python Script

A Python script that updates Spyglass deployments by reading configuration from a `model.yaml` file and making API calls to the Spyglass backend.

## Features
- Reads deployment configuration from `model.yaml`
- Uses environment variables for authentication and deployment targeting
- Makes authenticated API calls to update Spyglass deployments
- Provides detailed logging and error handling
- Supports both development and production API endpoints

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) for dependency management

## Installation

This project uses `uv` for dependency management. Install dependencies with:

```bash
uv sync
```

Or install the package in development mode:

```bash
uv pip install -e .
```

## Model Configuration File

Create a `model.yaml` file in your project root with the following structure:

```yaml
# Human-readable name for the deployment
name: "Production API"
# Description of the app
description: "Main production deployment handling customer requests"
# The model used in your app (e.g., "GPT-4", "Claude 3.5 Sonnet", "DeepSeek R1")
# This should be the string you are passing into your OpenAI client
model: "DeepSeek R1"
# The system prompt you are using in your application
prompt: |
  You are a helpful AI assistant that provides accurate and concise information.
  Always be polite and professional in your responses.
```

## Environment Variables

The script requires the following environment variables:

### Required
- `SPYGLASS_API_KEY`: Your Spyglass API authentication token
- `DEPLOYMENT_ID`: The ID of the deployment to update

### Optional
- `SPYGLASS_API_BASE_URL`: Base URL for the Spyglass API (defaults to `http://localhost:4000`)

## Running the Script

### Using uv

```bash
# Set environment variables
export SPYGLASS_API_KEY="your-api-key"
export DEPLOYMENT_ID="your-deployment-id"

# Run with uv
uv run python main.py
```

### Direct Python execution

If you have the dependencies installed:

```bash
export SPYGLASS_API_KEY="your-api-key"
export DEPLOYMENT_ID="your-deployment-id"
python main.py
```

### Production Environment

For production deployments, also set the API base URL:

```bash
export SPYGLASS_API_KEY="your-api-key"
export DEPLOYMENT_ID="your-deployment-id"
export SPYGLASS_API_BASE_URL="https://api.spyglass.ai"
uv run python main.py
```

## API Integration

The script makes a PUT request to `/api/deployments/{deployment_id}` with the following payload:

```json
{
  "name": "deployment name",
  "description": "deployment description",
  "model": "model name",
  "prompt": "system prompt"
}
```

Authentication is via `Authorization: Bearer {token}` header.

## Error Handling

The script provides comprehensive error handling for:

- Missing or invalid environment variables
- Missing or malformed `model.yaml` file
- Network connectivity issues
- API authentication failures
- API response errors

All errors are logged with descriptive messages and appropriate exit codes.

## Example Output

```
🚀 Starting Spyglass Deployment Action...
Updating deployment prod-api-v1 with:
  Model: DeepSeek R1
  Name: Production API
  Description: Main production deployment handling customer requests
  Prompt: You are a helpful AI assistant that provides accurate information...
✅ Successfully updated deployment prod-api-v1
   Status: 200
   Updated at: 2024-01-15T10:30:00Z
✨ Deployment update completed successfully!
```
