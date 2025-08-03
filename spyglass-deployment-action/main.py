import os
import sys
import time
import yaml
import requests
from typing import Dict, Any


def load_model_config(config_path: str) -> Dict[str, Any]:
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
    import os
    
    # Try multiple potential paths for the config file
    potential_paths = [
        config_path,  # Original path
        os.path.join("/github/workspace", config_path),  # GitHub Actions workspace
        os.path.join(os.getcwd(), config_path),  # Current directory
    ]
    
    # If we're in a GitHub Actions environment, also try the workspace directly
    if os.getenv("GITHUB_WORKSPACE"):
        potential_paths.append(os.path.join(os.getenv("GITHUB_WORKSPACE"), config_path))
    
    config_file_path = None
    for path in potential_paths:
        if os.path.exists(path):
            config_file_path = path
            print(f"🔍 Found config file at: {config_file_path}")
            break
        else:
            print(f"🔍 Tried path: {path} (not found)")
    
    if not config_file_path:
        print(f"❌ Could not find config file. Tried paths: {potential_paths}")
        raise FileNotFoundError(f"Config file not found at any of: {potential_paths}")
    
    try:
        with open(config_file_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
            
        if not isinstance(config, dict):
            raise ValueError("model.yaml must contain a YAML object/dictionary")
            
        return config
    except FileNotFoundError:
        import os
        current_dir = os.getcwd()
        files_in_dir = os.listdir(current_dir)
        print(f"Error: {config_path} not found in the current directory")
        print(f"Current working directory: {current_dir}")
        print(f"Files in current directory: {files_in_dir}")
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
    model_file_path = os.getenv("MODEL_FILE_PATH", "model.yaml")
    
    if not api_key:
        print("Error: SPYGLASS_API_KEY environment variable is required")
        sys.exit(1)
        
    if not deployment_id:
        print("Error: DEPLOYMENT_ID environment variable is required")
        sys.exit(1)
    
    api_base_url = os.getenv("SPYGLASS_API_BASE_URL", "https://api.spyglass-ai.com")
    
    return {
        "api_key": api_key,
        "deployment_id": deployment_id,
        "api_base_url": api_base_url,
        "model_file_path": model_file_path
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
                
            elif response.status_code in (401, 403):
                # Authentication/authorization error - don't retry
                print(f"❌ Authentication failed: Invalid API key")
                print(f"   Status: {response.status_code}")
                try:
                    error_data = response.json()
                    if "error" in error_data:
                        print(f"   Server message: {error_data['error']}")
                except:
                    print(f"   Response: {response.text}")
                print("   Please check that your SPYGLASS_API_KEY is valid and has the necessary permissions.")
                sys.exit(1)
                
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
    print(f"📄 Loading model configuration from: {env_vars['model_file_path']}")
    model_config = load_model_config(env_vars['model_file_path'])
    
    # Update the deployment
    update_spyglass_deployment(env_vars, model_config)
    
    print("✨ Deployment update completed successfully!")


if __name__ == "__main__":
    main()
