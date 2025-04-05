# app.py
from flask import Flask, request, redirect, render_template, jsonify
import redis
import uuid
import os

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    long_url = data.get('url')
    
    if not long_url:
        return jsonify({"error": "URL is required"}), 400
    
    short_id = str(uuid.uuid4())[:6]
    r.set(short_id, long_url)
    
    short_url = f"{request.host_url}{short_id}"
    return jsonify({"short_url": short_url})

@app.route('/<short_id>')
def redirect_to_long_url(short_id):
    long_url = r.get(short_id)
    if long_url:
        return redirect(long_url)
    return jsonify({"error": "URL not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)