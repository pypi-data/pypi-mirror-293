import os
import json

# Default configuration
DEFAULT_CONFIG = {
    "endpoint_url": "http://localhost:8000",
    "license_id": "123456",
    "license_secret": "abcdef"
}


def load_config():
    current_directory = os.getcwd()
    config_path = os.path.join(current_directory, "config.json")

    if not os.path.exists(config_path):
        with open(config_path, 'w') as config_file:
            json.dump(DEFAULT_CONFIG, config_file, indent=4)
        print(f"Config file created with default values at {config_path}")

    with open(config_path, 'r') as config_file:
        return json.load(config_file)


config = load_config()
ENDPOINT_URL = config.get("endpoint_url", DEFAULT_CONFIG["endpoint_url"])
LICENSE_ID = config.get("license_id", DEFAULT_CONFIG["license_id"])
LICENSE_SECRET = config.get("license_secret", DEFAULT_CONFIG["license_secret"])