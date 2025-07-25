from flask import Flask, jsonify, request, redirect
from models import store_url_mapping, get_original_url, increment_clicks, get_stats
from utils import generate_short_code, is_valid_url

app = Flask(__name__)

@app.route('/')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "URL Shortener API"
    })

@app.route('/api/health')
def api_health():
    return jsonify({
        "status": "ok",
        "message": "URL Shortener API is running"
    })

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'Missing URL'}), 400

    original_url = data['url']
    if not is_valid_url(original_url):
        return jsonify({'error': 'Invalid URL format'}), 400

    short_code = generate_short_code()
    store_url_mapping(short_code, original_url)

    return jsonify({
        'short_code': short_code,
        'short_url': f"http://localhost:5000/{short_code}"
    }), 201

@app.route('/<short_code>', methods=['GET'])
def redirect_to_original(short_code):
    mapping = get_original_url(short_code)
    if not mapping:
        return jsonify({'error': 'Short code not found'}), 404

    increment_clicks(short_code)
    return redirect(mapping['url'])

@app.route('/api/stats/<short_code>', methods=['GET'])
def get_url_stats(short_code):
    stats = get_stats(short_code)
    if not stats:
        return jsonify({'error': 'Short code not found'}), 404

    return jsonify({
        'url': stats['url'],
        'clicks': stats['clicks'],
        'created_at': stats['created_at']
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
