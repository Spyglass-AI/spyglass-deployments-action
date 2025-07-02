# Spyglass AI Deployment Action Script

A Python script that updates Spyglass deployments by reading configuration from a `model.yaml` file and making API calls to the Spyglass backend.

## Functionality
- Reads deployment configuration from `model.yaml`
- Uses environment variables for authentication and deployment targeting
- Makes authenticated API calls to update Spyglass Deployments dashboard
- Provides detailed logging and error handling

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
## Environment Variables

The script requires the following environment variables:

### Required
- `SPYGLASS_API_KEY`: Your Spyglass API authentication token
- `DEPLOYMENT_ID`: The ID of the deployment to update

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
