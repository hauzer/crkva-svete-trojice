from flask import Flask, url_for
from flask_session import Session
from markdown import markdown


class Config:
    DEBUG = True
    SECRET_KEY = 'head -c 32 /dev/random | base64'
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = 'sessions'


app = Flask(__name__)
app.config.from_object(Config)
app.config.from_envvar('{}_SETTINGS'.format(__name__.upper()), silent=True)

Session(app)


app.jinja_env.filters['markdown'] = markdown


@app.template_global()
def url_for_static(filename, *args, **kwargs):
    return url_for('static', *args, filename=filename, **kwargs)


app.add_template_global({
    'history':  'Историјат',
    'clergy':   'Свештенство',
    'parishes': 'Парохије',
    'schedule': 'Распоред',
    'contact':  'Контакт',
}, 'tabs')
