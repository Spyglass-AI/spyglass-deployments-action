# Spyglass AI Deployments GitHub Action

A GitHub Action for updating your Spyglass AI Deployments dashboard automatically based on the model configuration in your repo.

## Overview

This GitHub Action reads your model configuration from a `model.yaml` file in your repository and updates the corresponding deployment in the Spyglass AI platform.

## Quick Start

**Add to your workflow**: Create or update `.github/workflows/spyglass-deploy.yml` in your repo with this template. Fill in your `DEPLOYMENT_ID`, this should match the `DEPLOYMENT_ID` you use with the Spyglass SDK to send telemetry to the platform.

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

**Create model.yaml**: Add a `model.yaml` file to your repository root:

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

**Configure your API Key secret**:
1. Log in to your Spyglass dashboard
2. Navigate to Account > API Keys
3. Generate a new API key
4. Add it to your repository secrets as `SPYGLASS_API_KEY`

## Support

For issues with this GitHub Action, please [open an issue](https://github.com/spyglass-ai/spyglass-deployments-action/issues) in this repository.

For Spyglass AI platform support, contact [team@spyglass.ai](mailto:team@spyglass.ai).
