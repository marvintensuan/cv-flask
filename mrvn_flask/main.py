'''
My Curriculum Vitae Flask App
Author: Marvin D. Tensuan

GitHub: https://github.com/marvintensuan/cv-flask/
'''
import os
from flask import Flask, render_template, request, send_from_directory

# Initialize Flask app
app = Flask(__name__, static_folder='static', static_url_path='/' )

# Flask app routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/lifegoals')
def life_goals():
    return render_template('lifegoals.html')

@app.route('/intro')
def introductions():
    return render_template('introductions.html')

@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

# main entrypoint
port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)
