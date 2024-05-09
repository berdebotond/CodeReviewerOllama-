import json
import loguru
import re

from ollama import Client

from modules.config.app_config import AppConfig as cfg


def parse_json_from_ai_response(response: str) -> dict:
    """
    Parses the AI response and extracts the JSON content.
    Args:
    response (str): The AI response as a string.
    Returns:
    dict: The parsed JSON content as a dictionary.
    Raises:
    ValueError: If the response does not contain a valid JSON.
    """
    # looking between { and } using regex

    response = re.search(r'\{.*\}', response)
    if not response:
        loguru.logger.warning("No JSON response found")
        loguru.logger.debug(f"Error: No JSON response found in {response}")
        raise ValueError("No JSON response found")
    try:

        json_response = json.loads(response.group(0))

    except json.decoder.JSONDecodeError as e:
        loguru.logger.warning(f"Invalid JSON, error: {e}")
        loguru.logger.debug(f"Error: Invalid JSON response: {response}")
        raise ValueError(f"Invalid JSON response")

    return json_response


def ollama_chat(messages: list, system_prompt: str = None, try_outs: int = 5) -> dict:
    """
    This function sends a chat request to the Ollama API, appends a system message to the chat messages,
    and then parses the response into a JSON format. If the response contains a 'message' key, the function
    extracts the content of the message and parses it into a JSON format using the `parse_json_from_ai_response`
    function. If the response does not contain a 'message' key, or if the parsed JSON is invalid, the function
    raises a ValueError. The function also handles cases where the Ollama API fails to generate a JSON response
    after a certain number of attempts.

    :param system_prompt: json example for the model to answer the question in the json format
    :param messages: Messages with human and assistant messages
    :return: A dictionary containing the parsed JSON response from the Ollama chat
    :raises ValueError: If the response does not contain a valid JSON or if Ollama couldn't generate a JSON

    Args:
        try_outs:
    """
    client = Client(host='http://localhost:11434')
    messages.append({'role': 'system', 'content': system_prompt})
    try_out_index = 0
    while try_outs >= try_out_index:
        try:
            resp = client.chat(model=cfg.ollama_model, messages=messages, stream=False, format='json')
            if "message" in resp:
                try:
                    loguru.logger.debug(f"Response: {resp["message"]["content"]}")
                    json_resp = json.loads(resp["message"]["content"])
                except json.decoder.JSONDecodeError as e:
                    loguru.logger.warning(f"Invalid JSON response {e}")
                    json_resp = parse_json_from_ai_response(resp["message"]["content"])
                return json_resp
            else:
                loguru.logger.warning("No 'message' key found in the response")
                loguru.logger.debug(f"Error: No 'message' key found in the response: {resp}")
                raise ValueError("No 'message' key found in the response")

        except ValueError as e:
            loguru.logger.warning(f"Error: {e}")
            loguru.logger.debug(f"Error: {resp}")
        try_out_index += 1
    loguru.logger.warning(f"Error: Ollama couldn't generate a json")
    raise ValueError(f"Ollama couldn't generate a json")
