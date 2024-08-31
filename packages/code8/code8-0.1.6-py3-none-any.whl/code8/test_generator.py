import os
import json
import re
from openai import OpenAI
from anthropic import Anthropic
from pathlib import Path

def get_config_dir():
    return Path.home() / ".code8"

def get_config_file():
    return get_config_dir() / "config.json"

def load_config():
    config_file = get_config_file()
    if config_file.exists():
        with config_file.open('r') as f:
            return json.load(f)
    return {
        "api_key": "", 
        "model_provider": "", 
        "model": "",
        "system_prompt": "You are a helpful assistant that generates Python unit tests for the file named '{file_name}'. Do not include code blocks or explanations in your response, just the unittest code.",
        "user_prompt": "Please generate unit tests for the following Python code from the file '{file_name}':\n\n{code_content}\n\nProvide a complete unittest class with test methods for each function in the code.\nDo not include any explanations or code blocks, just the unittest code."
    }

def remove_code_blocks(text):
    # Remove ```python and ``` from the beginning and end of the text
    text = re.sub(r'^```python\n?', '', text, flags=re.MULTILINE)
    text = re.sub(r'\n?```$', '', text, flags=re.MULTILINE)
    return text

def generate_tests(input_file, system_prompt=None, user_prompt=None):
    config = load_config()
    api_key = config.get('api_key')
    model_provider = config.get('model_provider')
    model = config.get('model')

    if not api_key or not model_provider or not model:
        print("Please configure your settings by running 'code8' without arguments.")
        return

    file_name = os.path.basename(input_file)

    with open(input_file, 'r') as file:
        code_content = file.read()

    if system_prompt is None:
        system_prompt = config['system_prompt']
    if user_prompt is None:
        user_prompt = config['user_prompt']

    formatted_system_prompt = system_prompt.format(file_name=file_name)
    formatted_user_prompt = user_prompt.format(file_name=file_name, code_content=code_content)

    try:
        if model_provider == 'OpenAI':
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": formatted_system_prompt},
                    {"role": "user", "content": formatted_user_prompt}
                ]
            )
            test_code = response.choices[0].message.content
        elif model_provider == 'Anthropic':
            client = Anthropic(api_key=api_key)
            response = client.messages.create(
                model=model,
                max_tokens=4000,
                system=formatted_system_prompt,
                messages=[
                    {"role": "user", "content": formatted_user_prompt}
                ]
            )
            test_code = response.content[0].text
        else:
            raise ValueError(f"Unsupported model provider: {model_provider}")
    except Exception as e:
        print(f"Error calling API: {str(e)}")
        return

    test_code = remove_code_blocks(test_code)

    base_name = os.path.splitext(file_name)[0]
    test_file_name = f"test_{base_name}.py"

    with open(test_file_name, 'w') as test_file:
        test_file.write(test_code)

    print(f"Unit tests generated in {test_file_name}")