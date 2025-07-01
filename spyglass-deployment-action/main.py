import os
import sys
import time
import yaml
import requests
from typing import Dict, Any


def load_model_config(config_path: str = "model.yaml") -> Dict[str, Any]:
    """
    Load model configuration from YAML file.
    
    Args:
        config_path: Path to the model.yaml file
        
    Returns:
        Dictionary containing the model configuration
        
    Raises:
        FileNotFoundError: If model.yaml doesn't exist
        yaml.YAMLError: If YAML is invalid
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
            
        if not isinstance(config, dict):
            raise ValueError("model.yaml must contain a YAML object/dictionary")
            
        return config
    except FileNotFoundError:
        print(f"Error: {config_path} not found in the current directory")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading model configuration: {e}")
        sys.exit(1)


def get_environment_variables() -> Dict[str, str]:
    """
    Get required environment variables.
    
    Returns:
        Dictionary containing the environment variables
        
    Raises:
        SystemExit: If required environment variables are missing
    """
    api_key = os.getenv("SPYGLASS_API_KEY")
    deployment_id = os.getenv("DEPLOYMENT_ID")
    
    if not api_key:
        print("Error: SPYGLASS_API_KEY environment variable is required")
        sys.exit(1)
        
    if not deployment_id:
        print("Error: DEPLOYMENT_ID environment variable is required")
        sys.exit(1)
    
    # TODO: Make this our prod URL by default
    api_base_url = os.getenv("SPYGLASS_API_BASE_URL", "http://localhost:4000")
    
    return {
        "api_key": api_key,
        "deployment_id": deployment_id,
        "api_base_url": api_base_url
    }


def update_spyglass_deployment(env_vars: Dict[str, str], model_config: Dict[str, Any]) -> None:
    """
    Update Spyglass deployment via API call.
    
    Args:
        env_vars: Environment variables including API key and deployment ID
        model_config: Model configuration from YAML file
    """
    # Extract required fields from model config
    model = model_config.get("model")
    prompt = model_config.get("prompt")
    name = model_config.get("name")
    description = model_config.get("description")
    
    if not model:
        print("Error: 'model' field is required in model.yaml")
        sys.exit(1)
        
    if not prompt:
        print("Error: 'prompt' field is required in model.yaml")
        sys.exit(1)
        
    if not name:
        print("Error: 'name' field is required in model.yaml")
        sys.exit(1)
        
    if not description:
        print("Error: 'description' field is required in model.yaml")
        sys.exit(1)
    
    # Prepare API request
    url = f"{env_vars['api_base_url']}/api/deployments/{env_vars['deployment_id']}"
    
    headers = {
        "Authorization": f"Bearer {env_vars['api_key']}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "name": name,
        "model": model,
        "description": description,
        "prompt": prompt
    }
    
    print(f"Updating deployment {env_vars['deployment_id']} with:")
    print(f"  Model: {model}")
    print(f"  Name: {name}")
    print(f"  Description: {description}")
    print(f"  Prompt: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")
    
    max_retries = 3
    base_delay = 2  # seconds
    
    for attempt in range(max_retries):
        try:
            if attempt > 0:
                delay = base_delay * (2 ** (attempt - 1))  # Exponential backoff: 2s, 4s
                print(f"⏳ Retrying in {delay} seconds... (attempt {attempt + 1}/{max_retries})")
                time.sleep(delay)
            
            response = requests.put(url, json=payload, headers=headers, timeout=30)
            
            if response.status_code in (200, 201):
                print(f"✅ Successfully updated deployment {env_vars['deployment_id']}")
                print(f"   Status: {response.status_code}")
                if attempt > 0:
                    print(f"   Succeeded on attempt {attempt + 1}")
                
                # Print response data if available
                try:
                    response_data = response.json()
                    if "data" in response_data:
                        deployment_data = response_data["data"]
                        print(f"   Updated at: {deployment_data.get('updated_at', 'N/A')}")
                except:
                    pass  # Ignore JSON parsing errors for response data
                
                return  # Success - exit the function
                
            else:
                print(f"❌ API error on attempt {attempt + 1}: Status {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                except:
                    print(f"   Response: {response.text}")
                
                # If this was the last attempt, exit with error
                if attempt == max_retries - 1:
                    print(f"❌ Failed to update deployment after {max_retries} attempts")
                    sys.exit(1)
                    
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error on attempt {attempt + 1}: {e}")
            
            # If this was the last attempt, exit with error
            if attempt == max_retries - 1:
                print(f"❌ Failed to update deployment after {max_retries} attempts due to network errors")
                sys.exit(1)
                
        except Exception as e:
            print(f"❌ Unexpected error on attempt {attempt + 1}: {e}")
            
            # If this was the last attempt, exit with error
            if attempt == max_retries - 1:
                print(f"❌ Failed to update deployment after {max_retries} attempts due to unexpected errors")
                sys.exit(1)


def main():
    """
    Main function that orchestrates the deployment update process.
    """
    print("🚀 Starting Spyglass Deployment Action...")
    
    # Load environment variables
    env_vars = get_environment_variables()
    
    # Load model configuration
    model_config = load_model_config()
    
    # Update the deployment
    update_spyglass_deployment(env_vars, model_config)
    
    print("✨ Deployment update completed successfully!")


if __name__ == "__main__":
    main()
