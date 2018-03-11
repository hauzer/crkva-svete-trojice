from babel.dates import get_month_names
from flask import g, render_template, abort
from app import app
import articles


@app.route('/')
def index():
    g.articles = articles.get()['sorted-list']
    return render_template('index.html')


@app.route('/istorijat')
def history():
    return render_template('history.html')


@app.route('/svestenstvo')
def clergy():
    return render_template('clergy.html')


@app.route('/parohije')
def parishes():
    return render_template('parishes.html')


@app.route('/raspored')
def schedule():
    return render_template('schedule.html')


@app.route('/kontakt')
def contact():
    return render_template('contact.html')


@app.route('/objave/<int:year>')
def year(year):
    artcls = articles.get()
    if year in artcls['by-year']:
        g.articles = artcls['by-year'][year]['sorted-list']
        return render_template('year.html')

    return abort(404)


@app.route('/objave/<int:year>/<month_name>')
def month(year, month_name):
    artcls = articles.get()
    if year in artcls['by-year'] and \
            month_name in artcls['by-year'][year]['by-month-name']:
        g.articles = artcls['by-year'][year]['by-month-name'][month_name]['sorted-list']
        return render_template('month.html')

    return abort(404)


@app.route('/objava/<int:year>/<month_name>/<slug>')
def article(year, month_name, slug):
    artcls = articles.get()
    if year in artcls['by-year'] and \
            month_name in artcls['by-year'][year]['by-month-name'] and \
            slug in artcls['by-year'][year]['by-month-name'][month_name]['by-slug']:
        g.article = artcls['by-year'][year]['by-month-name'][month_name]['by-slug'][slug]
        return render_template('article.html')

    return abort(404)
