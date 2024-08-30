""" PlantUml Viewer"""

__version__ = "0.0.1" 

import os
import time
from flask import Flask, render_template, send_from_directory, jsonify



app = Flask(__name__)

# Set the directory to monitor
MONITOR_DIR = '/Users/fernando/ProcessMaker/repos/pm4_diagrams/out/tce'

# Function to get the list of PNG files
def get_png_files():
    return [f for f in os.listdir(MONITOR_DIR) if f.endswith('.png')]

# Route for the main page
@app.route('/')
def index():
    png_files = get_png_files()
    return render_template('index.html', png_files=png_files)

# Route to serve the images
@app.route('/images/<filename>')
def images(filename):
    return send_from_directory(MONITOR_DIR, filename)

# Route to check for file changes
@app.route('/check_file/<filename>')
def check_file(filename):
    file_path = os.path.join(MONITOR_DIR, filename)
    if os.path.exists(file_path):
        last_modified = os.path.getmtime(file_path)
        return jsonify({'last_modified': last_modified})
    return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)