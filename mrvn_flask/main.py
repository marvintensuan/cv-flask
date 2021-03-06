'''
My Curriculum Vitae Flask App
Author: Marvin D. Tensuan

GitHub: https://github.com/marvintensuan/cv-flask/
'''

import os
from datetime import datetime, timezone
from operator import itemgetter
from pathlib import Path
from flask import Flask, render_template, request, send_from_directory
from dotenv import load_dotenv

from google.cloud import firestore
import google.auth
from google.cloud import secretmanager as sm

try:
    # Get environment variables from Google Secret Manager,
    # write them in a .env file at the container, and load at runtime.
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_file = os.path.join(BASE_DIR, '.env')
    PROJECT_ID = '762981581825'
    SETTINGS_NAME = 'flask_app_settings'
    SECRET_VERSION = '6'

    if not os.path.isfile('.env'):
        _, project = google.auth.default()

        if project:
            client = sm.SecretManagerServiceClient()

            name = f"projects/{PROJECT_ID}/secrets/{SETTINGS_NAME}/versions/{SECRET_VERSION}"
            payload = client.access_secret_version(request={'name': name}).payload.data.decode("UTF-8")

            with open(env_file, "w") as f:
                f.write(payload)

    load_dotenv()

    # DB COLLECTION NAMES
    FIRESTORE_CPD = os.getenv('COLLECTION_NAME_CPD')
    FIRESTORE_OLC = os.getenv('COLLECTION_NAME_OLC')
    FIRESTORE_WEB = os.getenv('COLLECTION_NAME_WEB')
except Exception as e:
    print(f'An error occured. \n{e}')
    print('Failed to initialize variables.')

# Initialize Flask app
app = Flask(__name__, static_folder='static', static_url_path='/' )

# Initialize DB
db = firestore.Client()

# Helper
def create_context_from_db(collection):
    print(f'[Python]: Requested info from {collection}')
    context = []
    try:
        # Get data from Firestore
        collection_stream = db.collection(collection).stream()
        doc_list = [doc.to_dict() for doc in collection_stream]

        # Get 'date' key
        for key in doc_list[0]:
            if 'date' in key:
                KEY_SORTER = key

        # Assign temporary datetime values to None
        TEMP = datetime(1969, 7, 21, 20, 17, tzinfo=timezone.utc)
        for doc in doc_list:
            if doc[KEY_SORTER] is None:
                doc[KEY_SORTER] = TEMP

        # Sort values by date
        context = sorted(doc_list, key=itemgetter(KEY_SORTER), reverse=True)

        # Convert date values to str
        for doc in context:
            if doc[KEY_SORTER] == TEMP:
                doc[KEY_SORTER] = ''
            else:
                doc[KEY_SORTER] = doc[KEY_SORTER].strftime('%B %d, %Y')

    except Exception as e:
        print(f'[Python]: Exception occured for {collection}')
        print(e)
    finally:
        return context

# Flask app routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/list_of_cpds')
def learning_cpd():
    context_cpd = create_context_from_db(FIRESTORE_CPD)
    return render_template('list_of_cpds.html', context_cpd = context_cpd)

@app.route('/self_directed_learning')
def learning_sdl():
    olc = create_context_from_db(FIRESTORE_OLC)
    web = create_context_from_db(FIRESTORE_WEB)
    context_sdl = {
        'online_courses' : olc,
        'webinars' : web
    }
    return render_template('self_directed_learning.html', context_sdl = context_sdl)

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
