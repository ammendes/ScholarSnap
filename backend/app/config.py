import yaml


# Open and read configuration from config.yaml
with open("config.yaml") as f:
    config = yaml.safe_load(f)

OLLAMA_API_URL = config["ollama"]["url"]
OLLAMA_MODEL = config["ollama"]["model"]
ARXIV_API_URL = config["arxiv"]["api_url"]
DEFAULT_DAYS = config["arxiv"]["default_days"]
BATCH_SIZE = config["arxiv"]["batch_size"]

