import dataclasses

@dataclasses.dataclass
class AppConfig:
    # ollama_client configuration
    ollama_model: str = 'llama3'