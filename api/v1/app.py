#!/usr/bin/python3
from flask import Flask, jsonify
from api.v1.views import app_views
import os
from models import storage

app = Flask(__name__)

# Register the blueprint for API routes
app.register_blueprint(app_views)

# Teardown app context function to close the storage session after each request
@app.teardown_appcontext
def teardown_appcontext(exception):
    """
    Close the storage session after each request.
    """
    storage.close()

# Custom 404 error handler that returns a JSON response
@app.errorhandler(404)
def errorhandler404(exception):
    """
    Custom 404 error handler that returns a JSON response.

    Returns:
        JSON response with a 404 status code and an error message.
    """
    return jsonify(error='Not found'), 404

if __name__ == "__main__":
    # Get host and port from environment variables, defaulting to '0.0.0.0' and 5000
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', '5000'))

    # Run the Flask application
    app.run(host=host, port=port, threaded=True)
