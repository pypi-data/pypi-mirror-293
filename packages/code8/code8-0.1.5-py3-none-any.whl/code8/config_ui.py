import os
import json
import socket
import asyncio
import webbrowser
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from .test_generator import generate_tests, load_config

app = Flask(__name__)

def get_config_dir():
    return Path.home() / ".code8"

def get_config_file():
    return get_config_dir() / "config.json"

def get_profiles_file():
    return get_config_dir() / "profiles.json"

def ensure_config_dir():
    config_dir = get_config_dir()
    config_dir.mkdir(parents=True, exist_ok=True)

def load_profiles():
    profiles_file = get_profiles_file()
    if profiles_file.exists():
        with profiles_file.open('r') as f:
            return json.load(f)
    return {'Default': load_config()}

def save_profiles(profiles):
    ensure_config_dir()
    with get_profiles_file().open('w') as f:
        json.dump(profiles, f)

def load_config():
    config_file = get_config_file()
    if config_file.exists():
        with config_file.open('r') as f:
            return json.load(f)
    return {}  # Return default config or empty dict

@app.route('/')
def index():
    config = load_config()
    return render_template('index.html', config=config)

@app.route('/save', methods=['POST'])
def save():
    config = request.json
    ensure_config_dir()
    with get_config_file().open('w') as f:
        json.dump(config, f)
    return jsonify({"status": "success"})

@app.route('/browse')
def browse():
    path = request.args.get('path', '.')
    items = []
    for item in os.listdir(path):
        full_path = os.path.join(path, item)
        items.append({
            'name': item,
            'path': full_path,
            'type': 'directory' if os.path.isdir(full_path) else 'file'
        })
    return jsonify(items)

@app.route('/run_tests', methods=['POST'])
def run_tests():
    files = request.json['files']
    config = load_config()
    
    async def run_tests_async():
        tasks = [asyncio.to_thread(generate_tests, file, config['system_prompt'], config['user_prompt']) for file in files]
        await asyncio.gather(*tasks)
    
    asyncio.run(run_tests_async())
    return jsonify({"status": "success", "message": f"Tests generated for {len(files)} files"})

@app.route('/get_profiles', methods=['GET'])
def get_profiles():
    profiles = load_profiles()
    return jsonify([{'id': name, 'name': name} for name in profiles.keys()])

@app.route('/load_profile/<id>', methods=['GET'])
def load_profile(id):
    profiles = load_profiles()
    if id not in profiles:
        return jsonify({"error": "Profile not found"}), 404
    return jsonify(profiles[id])

@app.route('/get_profile/<id>', methods=['GET'])
def get_profile(id):
    profiles = load_profiles()
    if id not in profiles:
        return jsonify({"error": "Profile not found"}), 404
    profile = profiles[id]
    profile['id'] = id
    profile['name'] = id
    return jsonify(profile)

@app.route('/save_profile', methods=['POST'])
def save_profile():
    data = request.json
    profiles = load_profiles()
    
    if data['id'] == 'Default':
        return jsonify({"error": "Cannot modify Default profile"}), 400
    
    old_name = data['id']
    new_name = data['name']
    
    if old_name != new_name:
        if old_name in profiles:
            del profiles[old_name]
        if new_name in profiles:
            return jsonify({"error": f"Profile '{new_name}' already exists"}), 400
    
    profiles[new_name] = {
        'api_key': data['api_key'],
        'model_provider': data['model_provider'],
        'model': data['model'],
        'system_prompt': data['system_prompt'],
        'user_prompt': data['user_prompt']
    }
    
    save_profiles(profiles)
    return jsonify({"status": "success"})

@app.route('/delete_profile/<id>', methods=['DELETE'])
def delete_profile(id):
    if id == 'Default':
        return jsonify({"error": "Cannot delete Default profile"}), 400
    
    profiles = load_profiles()
    if id not in profiles:
        return jsonify({"error": "Profile not found"}), 404
    
    del profiles[id]
    save_profiles(profiles)
    return jsonify({"status": "success"})

def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

def run_config_ui():
    port = find_free_port()
    webbrowser.open(f'http://127.0.0.1:{port}/')
    app.run(port=port, debug=False)

if __name__ == '__main__':
    run_config_ui()