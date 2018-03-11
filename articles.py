from babel.dates import get_month_names
from datetime import datetime

from itertools import groupby
import os
import re

from markdown import markdown
from slugify_sr_cyrl import slugify_sr_cyrl
from app import app


class Article:
    def __init__(self, path):
        self.filename = os.path.basename(path)
        filename_parse = re.match('^(\d{4}-\d{2}-\d{2}) (.+?)\.md$', self.filename).groups()

        self.title = filename_parse[1]
        self.date = datetime.strptime(filename_parse[0], '%Y-%m-%d')
        self.month_name = {
            'cyrl': get_month_names('wide', locale='sr_Cyrl_RS')[self.date.month],
            'latn': get_month_names('wide', locale='sr_Latn_RS')[self.date.month],
        }

        with open(path, 'r') as content:
            self.content = markdown(content.read())
        self.excerpt = '\n'.join(self.content.splitlines()[:5])
        self.is_short = self.content == self.excerpt

        self.slug = slugify_sr_cyrl(self.title)


def collect():
    month_names = get_month_names('wide', locale='sr_Latn_RS')

    articles = {}
    articles['sorted-list'] = []
    articles_dir = os.path.join(app.root_path, 'articles')
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


articles = collect()


def get():
    return articles
