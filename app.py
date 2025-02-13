from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, session
from utils.story_generator import StoryGenerator
from utils.config import AVAILABLE_MODELS, EXPERTISE_LEVELS, TONE_STYLES
from dotenv import load_dotenv
import os
import io

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', os.urandom(24))  # Get from env or generate
load_dotenv()

def get_api_key():
    return os.getenv('GEMINI_API_KEY') or session.get('api_key')

@app.route('/')
def index():
    api_key = get_api_key()
    if not api_key:
        return redirect(url_for('setup'))
        
    return render_template('index.html',
                         models=AVAILABLE_MODELS,
                         expertise_levels=EXPERTISE_LEVELS,
                         tone_styles=TONE_STYLES)

@app.route('/setup', methods=['GET', 'POST'])
def setup():
    if request.method == 'POST':
        api_key = request.form.get('api_key')
        if api_key:
            session['api_key'] = api_key
            return redirect(url_for('index'))
    return render_template('setup.html')

@app.route('/generate', methods=['POST'])
def generate_story():
    try:
        api_key = get_api_key()
        if not api_key:
            return jsonify({
                'error': 'API key not found. Please set up your API key first.'
            }), 401

        data = request.json
        topic = data.get('topic')
        model_name = data.get('model', 'gemini-2.0-flash-exp')
        expertise = data.get('expertise')
        tone = data.get('tone')
        context = data.get('context', '')
        total_parts = int(data.get('total_parts', 3))

        if not all([topic, expertise, tone]):
            return jsonify({
                'error': 'Missing required fields'
            }), 400

        generator = StoryGenerator(model_name, api_key)
        story = generator.generate_complete_story(
            topic=topic,
            expertise=expertise,
            tone=tone,
            context=context,
            total_parts=total_parts
        )

        return jsonify({
            'success': True,
            'story': story
        })

    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/download', methods=['POST'])
def download_story():
    try:
        story = request.json.get('story', '')
        if not story:
            return jsonify({'error': 'No story content provided'}), 400

        # Create in-memory file
        file_stream = io.StringIO(story)
        return send_file(
            io.BytesIO(file_stream.getvalue().encode('utf-8')),
            mimetype='text/plain',
            as_attachment=True,
            download_name='generated_story.txt'
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)