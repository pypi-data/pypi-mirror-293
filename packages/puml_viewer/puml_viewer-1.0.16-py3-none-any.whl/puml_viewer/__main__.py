
import os
import logging
from flask import Flask, render_template, send_from_directory, jsonify



app = Flask(__name__)

current_directory = os.getcwd()
app.logger(f"Current directory: {current_directory}")

# Set the directory to monitor
MONITOR_DIR = current_directory

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

def main():
    app.run(debug=False)
    #app.run(debug=True)    

if __name__ == '__main__':
    main()    