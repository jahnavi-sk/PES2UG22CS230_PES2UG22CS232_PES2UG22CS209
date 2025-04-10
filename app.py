from flask import Flask, request, redirect, render_template, jsonify
import redis
import uuid
import os
import logging
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Use environment variables for Redis connection with defaults
redis_host = os.environ.get('REDIS_HOST', 'localhost')
redis_port = int(os.environ.get('REDIS_PORT', 6379))
redis_password = os.environ.get('REDIS_PASSWORD', None)

# Connect to Redis with password if provided
try:
    r = redis.Redis(
        host=redis_host, 
        port=redis_port, 
        password=redis_password, 
        decode_responses=True
    )
    # Test Redis connection
    r.ping()
    logger.info("Successfully connected to Redis")
except Exception as e:
    logger.error(f"Failed to connect to Redis: {e}")
    # Still create the Redis client, but log the error
    r = redis.Redis(
        host=redis_host, 
        port=redis_port, 
        password=redis_password, 
        decode_responses=True
    )

# Configuration for the domain name (can be set via environment variable)
DOMAIN_NAME = os.environ.get('DOMAIN_NAME', None)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/shorten', methods=['POST'])
def api_shorten_url():
    data = request.get_json()
    long_url = data.get('url')
    
    if not long_url:
        return jsonify({"error": "URL is required"}), 400
    
    # Ensure the URL has a scheme
    if not long_url.startswith(('http://', 'https://')):
        long_url = 'http://' + long_url
    
    # Generate a shorter ID for better usability
    short_id = str(uuid.uuid4())[:6]
    logger.info(f"Creating short URL: {short_id} -> {long_url}")
    
    try:
        # Store the URL in Redis
        r.set(short_id, long_url)
        logger.info(f"Successfully stored in Redis: {short_id}")
    except Exception as e:
        logger.error(f"Failed to store in Redis: {e}")
        return jsonify({"error": "Failed to store URL"}), 500
    
    # Determine the base URL to use for the shortened URL
    if DOMAIN_NAME:
        # For indianexpress.com, create a path-based URL
        if DOMAIN_NAME == "indianexpress.com":
            base_url = f"https://{DOMAIN_NAME}/"
        else:
            # Use configured domain if available
            base_url = f"http://{DOMAIN_NAME}/"
    else:
        # Extract host and port from request
        host = request.host
        scheme = request.scheme
        base_url = f"{scheme}://{host}/"
    
    # Create shortened URL with the appropriate base URL
    short_url = f"{base_url}{short_id}"
    logger.info(f"Generated short URL: {short_url}")
    
    return jsonify({"short_url": short_url})

# Keep the original /shorten route for compatibility
@app.route('/shorten', methods=['POST'])
def shorten_url():
    return api_shorten_url()

@app.route('/<short_id>')
def redirect_to_long_url(short_id):
    logger.info(f"Attempting to redirect short ID: {short_id}")
    
    try:
        # Retrieve the original URL from Redis
        long_url = r.get(short_id)
        logger.info(f"Retrieved from Redis: {short_id} -> {long_url}")
    except Exception as e:
        logger.error(f"Error retrieving from Redis: {e}")
        return jsonify({"error": "Failed to retrieve URL from database"}), 500
    
    if long_url:
        logger.info(f"Redirecting to: {long_url}")
        return redirect(long_url)
    else:
        logger.warning(f"URL not found for short ID: {short_id}")
        return render_template('error.html', message="URL not found"), 404

@app.route('/api/delete/<short_id>', methods=['DELETE'])
def delete_url(short_id):
    try:
        # Check if the URL exists before trying to delete
        if r.exists(short_id):
            r.delete(short_id)
            return jsonify({"success": True, "message": f"URL with ID {short_id} deleted successfully"}), 200
        else:
            return jsonify({"error": "URL not found"}), 404
    except Exception as e:
        logger.error(f"Error deleting from Redis: {e}")
        return jsonify({"error": "Failed to delete URL from database"}), 500

if __name__ == '__main__':
    # Log the domain configuration
    if DOMAIN_NAME:
        logger.info(f"Using configured domain: {DOMAIN_NAME}")
    else:
        logger.info("No domain configured, using request host")
    
    app.run(host='0.0.0.0', debug=False)