# spyglass-deployments-action

A GitHub Action for updating your Spyglass AI Deployments automatically based on your model configuration.

## Overview

This GitHub Action reads your AI model configuration from a `model.yaml` file in your repository and updates the corresponding deployment in Spyglass. It's designed to keep your Spyglass deployments in sync with your codebase changes.

## Quick Start

1. **Add to your workflow**: Create or update `.github/workflows/spyglass-deploy.yml`

```yaml
name: Update Spyglass Deployment

on:
  push:
    branches:
      - main

jobs:
  spyglass-deployments:
    runs-on: ubuntu-latest
    name: Update Spyglass Deployments
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        
      - name: Update Spyglass Deployments
        uses: spyglass-ai/spyglass-deployments-action@v1
        env:
          SPYGLASS_API_KEY: ${{ secrets.SPYGLASS_API_KEY }}
          DEPLOYMENT_ID: 'your-deployment-id'
```

2. **Create model.yaml**: Add a `model.yaml` file to your repository root:

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

3. **Configure secrets**: Add your `SPYGLASS_API_KEY` to your repository secrets

## Configuration

### Environment Variables

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `SPYGLASS_API_KEY` | Yes | Your Spyglass API authentication token | - |
| `DEPLOYMENT_ID` | Yes | The ID of the deployment to update | - |
| `SPYGLASS_API_BASE_URL` | No | Base URL for the Spyglass API | `http://localhost:4000` |

### Model Configuration (`model.yaml`)

| Field | Required | Description |
|-------|----------|-------------|
| `model` | Yes | The AI model identifier (should match your OpenAI client config) |
| `prompt` | Yes | The system prompt for your AI model |
| `name` | No | Human-readable name for the deployment |
| `description` | No | Description of the deployment's purpose |

## Advanced Usage

### Multiple Deployments

You can run the action multiple times for different deployments:

```yaml
jobs:
  deploy-production:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Update Production Deployment
        uses: spyglass-ai/spyglass-deployments-action@v1
        env:
          SPYGLASS_API_KEY: ${{ secrets.SPYGLASS_API_KEY }}
          DEPLOYMENT_ID: 'prod-api-v1'
          
  deploy-staging:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Update Staging Deployment
        uses: spyglass-ai/spyglass-deployments-action@v1
        env:
          SPYGLASS_API_KEY: ${{ secrets.SPYGLASS_API_KEY }}
          DEPLOYMENT_ID: 'staging-api-v1'
```

### Custom Model File Location

By default, the action looks for `model.yaml` in the repository root. You can specify a different location by modifying the Python script in your fork.

### Production API Endpoint

For production use, set the `SPYGLASS_API_BASE_URL` environment variable:

```yaml
env:
  SPYGLASS_API_KEY: ${{ secrets.SPYGLASS_API_KEY }}
  DEPLOYMENT_ID: 'your-deployment-id'
  SPYGLASS_API_BASE_URL: 'https://api.spyglass.ai'
```

## Getting Your API Key

1. Log in to your Spyglass dashboard
2. Navigate to Settings > API Keys
3. Generate a new API key
4. Add it to your repository secrets as `SPYGLASS_API_KEY`

## Getting Your Deployment ID

1. Go to your Spyglass dashboard
2. Navigate to the Deployments section
3. Copy the deployment ID from the deployment you want to update

## Development

See the [Python script README](./spyglass-deployment-action/README.md) for details on developing and testing the underlying script.

## Support

For issues with this GitHub Action, please [open an issue](https://github.com/spyglass-ai/spyglass-deployments-action/issues) in this repository.

For Spyglass platform support, contact [support@spyglass.ai](mailto:support@spyglass.ai).
