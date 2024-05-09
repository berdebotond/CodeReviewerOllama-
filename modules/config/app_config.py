import dataclasses


@dataclasses.dataclass
class AppConfig:
    # ollama_client configuration
    code_generator = 'Analyse the following code in json format {"improvements": "", "bugs": "", "code_quality": ""}:'
    ollama_model: str = 'llama3'
    system_prompt: str = ('Your a developer, who does code review, your task is to analyse the given code and '
                          'answer in the following json, the valus can beb null, {"improvements": "", "bugs": "", '
                          '"code_quality": ""}')

