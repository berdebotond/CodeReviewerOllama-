from unittest.mock import patch

import pytest
import json
import re

from modules.ollama_client.ollama_client import parse_json_from_ai_response, ollama_chat


def test_valid_json_response():
    response = 'dsfsdggdsgsd dsgfdf sefd{"key1": "value1", "key2": "value2"}sdgdgsgds'
    expected_output = {'key1': 'value1', 'key2': 'value2'}
    assert parse_json_from_ai_response(response) == expected_output


def test_invalid_json_response():
    response = '{"key1": "value1,"value2"}'
    with pytest.raises(ValueError):
        parse_json_from_ai_response(response)


def test_no_json_response():
    response = 'No JSON response here'
    with pytest.raises(ValueError):
        parse_json_from_ai_response(response)


# Test valid response with correct JSON
def test_ollama_chat_valid_response():
    with patch('modules.ollama_client.ollama_client.Client') as MockClient:
        mock_client = MockClient.return_value
        mock_client.chat.return_value = {"message": {"content": '{"key": "value"}'}}
        messages = [{'role': 'user', 'content': 'Hello'}]
        json_example = '{"key": "value"}'
        assert ollama_chat(messages, json_example) == {"key": "value"}


# Test response without 'message' key
def test_ollama_chat_no_message_key():
    with patch('modules.ollama_client.ollama_client.Client') as MockClient:
        mock_client = MockClient.return_value
        mock_client.chat.return_value = {}
        messages = [{'role': 'user', 'content': 'Hello'}]
        json_example = '{"key": "value"}'
        with pytest.raises(ValueError) as excinfo:
            ollama_chat(messages, json_example)
        assert "Ollama couldn't generate a json" in str(excinfo.value)


# Test response with invalid JSON
def test_ollama_chat_invalid_json():
    with patch('modules.ollama_client.ollama_client.Client') as MockClient:
        mock_client = MockClient.return_value
        mock_client.chat.return_value = {"message": {"content": 'Invalid JSON'}}
        messages = [{'role': 'user', 'content': 'Hello'}]
        json_example = '{"key": "value"}'
        with pytest.raises(ValueError) as excinfo:
            ollama_chat(messages, json_example)
        assert "Ollama couldn't generate a json" in str(excinfo.value)


# Test retries and failure to generate a JSON
def test_ollama_chat_failure_to_generate_json():
    with patch('modules.ollama_client.ollama_client.Client') as MockClient:
        mock_client = MockClient.return_value
        mock_client.chat.side_effect = [{} for _ in range(6)]  # Simulate failing to generate JSON more than `try_outs`
        messages = [{'role': 'user', 'content': 'Hello'}]
        json_example = '{"key": "value"}'
        with pytest.raises(ValueError) as excinfo:
            ollama_chat(messages, json_example, try_outs=5)
        assert "Ollama couldn't generate a json" in str(excinfo.value)