#!/usr/bin/env python3
"""
Stata Llama Editor - Web Application
Flask web server for the Stata code assistant
"""

from flask import Flask, render_template, request, Response, jsonify
import sys
from pathlib import Path
import json

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from llama_client import LlamaClient
from stata_helper import StataHelper

app = Flask(__name__, 
            template_folder='../templates',
            static_folder='../static')

# Initialize clients
llama_client = LlamaClient()
stata_helper = StataHelper()


@app.route('/')
def index():
    """Render the main chat interface"""
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages with streaming response"""
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    # Enhance prompt with Stata context
    enhanced_prompt = stata_helper.enhance_prompt(user_message)
    
    def generate():
        """Stream the response"""
        try:
            for chunk in llama_client.stream_generate(enhanced_prompt):
                # Send each chunk as JSON
                yield f"data: {json.dumps({'content': chunk})}\n\n"
            
            # Signal completion
            yield f"data: {json.dumps({'done': True})}\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return Response(generate(), mimetype='text/event-stream')


@app.route('/api/commands/<command>', methods=['POST'])
def handle_command(command):
    """Handle special commands like /explain, /fix, /optimize"""
    data = request.json
    code = data.get('code', '')
    
    if not code:
        return jsonify({'error': 'No code provided'}), 400
    
    # Build prompt based on command
    prompts = {
        'explain': f"Please explain this Stata code:\n\n{code}",
        'fix': f"Please debug and fix this Stata code:\n\n{code}",
        'optimize': f"Please suggest optimizations for this Stata code:\n\n{code}"
    }
    
    if command not in prompts:
        return jsonify({'error': f'Unknown command: {command}'}), 400
    
    prompt = prompts[command]
    
    def generate():
        """Stream the response"""
        try:
            for chunk in llama_client.stream_generate(prompt):
                yield f"data: {json.dumps({'content': chunk})}\n\n"
            
            yield f"data: {json.dumps({'done': True})}\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return Response(generate(), mimetype='text/event-stream')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Check if the service is running"""
    return jsonify({
        'status': 'healthy',
        'model': llama_client.model_name,
        'ollama_host': llama_client.ollama_host
    })


if __name__ == '__main__':
    print("🚀 Starting Stata Llama Editor Web Interface...")
    print("📍 Open your browser to: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
