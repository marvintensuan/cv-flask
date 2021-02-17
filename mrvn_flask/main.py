'''
My Flask App
Author: Marvin D. Tensuan
'''

import os
from flask import Flask, render_template, request, send_from_directory
from dotenv import load_dotenv

try:
    from google.cloud import firestore
except:
    print('Cannot import google.cloud.firestore')

try:
    '''
    Get environment variables from Google Secret Manager,
    write them in a .env file at the container, and load at runtime.
    '''
    import google.auth
    from google.cloud import secretmanager as sm

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_file = os.path.join(BASE_DIR,  ".env")
    SETTINGS_NAME = "flask_app_settings"

    if not os.path.isfile('.env'):
        _, project = google.auth.default()

        if project:
            client = sm.SecretManagerServiceClient()
            path = client.secret_version_path(project, SETTINGS_NAME, "latest")
            payload = client.access_secret_version(path).payload.data.decode("UTF-8")

            with open(env_file, "w") as f:
                f.write(payload)
        
    load_dotenv()
    # DB COLLECTION NAMES
    FIRESTORE_CPD = os.getenv('COLLECTION_NAME_CPD')
    FIRESTORE_OLC = os.getenv('COLLECTION_NAME_OLC')
    FIRESTORE_WEB = os.getenv('COLLECTION_NAME_WEB')

except ImportError:
    print("Import Error raised.")

# Initialize Flask app
app = Flask(__name__, static_folder='static', static_url_path='/' )

# Initialize DB
db = firestore.Client()


# Flask app routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/list_of_cpds')
def learning_cpd():
    cpd_collection = db.collection(FIRESTORE_CPD).stream()
    context_cpd = [doc.to_dict() for doc in cpd_collection]
    return render_template('list_of_cpds.html', context = context_cpd)

@app.route('/self_directed_learning')
def learning_sdl():
    return render_template('self_directed_learning.html')

@app.route('/my_learning_roadmap')
def learning_roadmap():
    return render_template('my_learning_roadmap.html')

@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


# main entrypoint
port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)