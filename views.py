from flask import g, render_template, abort
from app import app
import articles


@app.route('/')
def index():
    g.article = articles.collection['sorted-list'][0]
    return render_template('index.html')


@app.route('/dogadjaji')
def archive():
    g.articles = articles.collection['sorted-list']
    return render_template('archive.html')


@app.route('/istorijat')
def history():
    return render_template('history.html')


@app.route('/svestenstvo')
def clergy():
    return render_template('clergy.html')


@app.route('/parohije')
def parishes():
    return render_template('parishes.html')


@app.route('/bogosluzenje')
def schedule():
    return render_template('schedule.html')


@app.route('/mapa')
def map():
    return render_template('map.html')


@app.route('/objave/<int:year>')
def year(year):
    if year in articles.collection['by-year']:
        g.articles = articles.collection['by-year'][year]['sorted-list']
        return render_template('year.html')

    return abort(404)


@app.route('/objave/<int:year>/<month_name>')
def month(year, month_name):
    if year in articles.collection['by-year'] and \
            month_name in articles.collection['by-year'][year]['by-month-name']:
        g.articles = articles.collection['by-year'][year]['by-month-name'][month_name]['sorted-list']
        return render_template('month.html')

    return abort(404)


@app.route('/objava/<int:year>/<month_name>/<slug>')
def article(year, month_name, slug):
    if year in articles.collection['by-year'] and \
            month_name in articles.collection['by-year'][year]['by-month-name'] and \
            slug in articles.collection['by-year'][year]['by-month-name'][month_name]['by-slug']:
        g.article = articles.collection['by-year'][year]['by-month-name'][month_name]['by-slug'][slug]
        return render_template('article.html')

    return abort(404)
