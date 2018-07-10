from babel.dates import get_month_names
from datetime import datetime

from itertools import groupby
import os
import re

from bs4 import BeautifulSoup
from slugify_sr_cyrl import slugify_sr_cyrl
from app import app


ARTICLES_DIR = 'articles'


class Article:
    def __init__(self, path):
        self.filename = os.path.basename(path)
        self.path = os.path.join(ARTICLES_DIR, self.filename)
        filename_re_groups = re.match('^(\d{4}-\d{2}-\d{2}) (.+?)\.html$', self.filename).groups()

        self.title = filename_re_groups[1]
        self.date = datetime.strptime(filename_re_groups[0], '%Y-%m-%d')
        self.month_name = {
            'cyrl': get_month_names('wide', locale='sr_Cyrl_RS')[self.date.month],
            'latn': get_month_names('wide', locale='sr_Latn_RS')[self.date.month],
        }

        self.aprox_size = None
        self.slug = slugify_sr_cyrl(self.title)

    @property
    def is_short(self):
        if not self.aprox_size:
            bs = BeautifulSoup(app.jinja_env.get_template(self.path).render(), 'html.parser')

            self.aprox_size = 0
            self.aprox_size += len(bs.find_all('span', class_='image')) * 300
            for p in bs.find_all('p'):
                self.aprox_size += len(p.text) * 0.3

        return self.aprox_size <= 600


def collect():
    articles = {}
    articles['sorted-list'] = []
    articles_dir = os.path.join(app.template_folder, ARTICLES_DIR)
    _, _, article_files = next(os.walk(articles_dir))
    for article_file in sorted(article_files, reverse=True):
        article_path = os.path.join(articles_dir, article_file)
        articles['sorted-list'].append(Article(article_path))

    articles['by-year'] = {}
    for year, articles_by_year in groupby(articles['sorted-list'], lambda a: a.date.year):
        articles_by_year = list(articles_by_year)
        articles['by-year'][year] = {}
        articles['by-year'][year]['sorted-list'] = articles_by_year
        articles['by-year'][year]['by-month'] = {}
        articles['by-year'][year]['by-month-name'] = {}

        month_names = get_month_names('wide', locale='sr_Latn_RS')
        for month, articles_by_month in groupby(articles_by_year, lambda a: a.date.month):
            articles_by_month = list(articles_by_month)

            articles['by-year'][year]['by-month'][month] = {}
            articles['by-year'][year]['by-month'][month]['sorted-list'] = articles_by_month
            articles['by-year'][year]['by-month'][month]['by-slug'] = \
                {article.slug: article for article in articles_by_month}

            month_name = month_names[month]
            articles['by-year'][year]['by-month-name'][month_name] = {}
            articles['by-year'][year]['by-month-name'][month_name]['sorted-list'] = \
                articles['by-year'][year]['by-month'][month]['sorted-list']
            articles['by-year'][year]['by-month-name'][month_name]['by-slug'] = \
                articles['by-year'][year]['by-month'][month]['by-slug']

    return articles


collection = collect()
