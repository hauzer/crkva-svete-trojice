from flask import Flask, g, url_for
from flask_session import Session
from flask_misaka import Misaka


class Config:
    DEBUG = True
    SECRET_KEY = 'head -c 32 /dev/random | base64'
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = 'sessions'


app = Flask(__name__)
app.config.from_object(Config)
app.config.from_envvar('{}_SETTINGS'.format(__name__.upper()), silent=True)

Session(app)
Misaka(app)


@app.before_request
def set_images_counter():
    g.n_images = [1]


@app.template_global()
def url_for_static(filename, *args, **kwargs):
    return url_for('static', *args, filename=filename, **kwargs)


app.add_template_global({
    'archive':  'Догађаји',
    'history':  'Историјат',
    'clergy':   'Свештенство',
    # 'schedule': 'Богослужење',
    'map':     'Мапа',
}, 'tabs')
