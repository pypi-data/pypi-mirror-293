import os
import json
import asyncio
import webbrowser
from flask import Flask, render_template, request, jsonify
from .test_generator import generate_tests, load_config

app = Flask(__name__)

CONFIG_FILE = 'config.json'
PROFILES_FILE = 'profiles.json'

def load_profiles():
    if os.path.exists(PROFILES_FILE):
        with open(PROFILES_FILE, 'r') as f:
            return json.load(f)
    return {'Default': load_config()}

def save_profiles(profiles):
    with open(PROFILES_FILE, 'w') as f:
        json.dump(profiles, f)

@app.route('/')
def index():
    config = load_config()
    return render_template('index.html', config=config)

@app.route('/save', methods=['POST'])
def save():
    config = request.json
    with open(CONFIG_FILE, 'w') as f:
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
    profile['name'] = id  # Add this line to include the name
    return jsonify(profile)

@app.route('/save_profile', methods=['POST'])
def save_profile():
    data = request.json
    profiles = load_profiles()
    
    if data['id'] == 'Default':
        return jsonify({"error": "Cannot modify Default profile"}), 400
    
    old_name = data['id']
    new_name = data['name']
    
    # If the name is changed, remove the old profile and create a new one
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

def run_config_ui():
    webbrowser.open('http://127.0.0.1:5000/')
    app.run(debug=False)

if __name__ == '__main__':
    run_config_ui()