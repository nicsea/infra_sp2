import csv

from django.core.management.base import BaseCommand
from django.db import IntegrityError

from reviews.models import Category, Genre, Title, GenreTitle, User, Comment, \
    Review

import_dict = {
    'genre': (Genre, 'genre.csv',
              ('id', 'name', 'slug',)),
    'category': (Category, 'category.csv',
                 ('id', 'name', 'slug',)),
    'titles': (Title, 'titles.csv',
               ('id', 'name', 'year', 'category_id',)),
    'genre_title': (GenreTitle, 'genre_title.csv',
                    ('id', 'title_id', 'genre_id',)),
    'users': (User, 'users.csv', ('id', 'username', 'email', 'role',
                                  'bio', 'first_name', 'last_name')),
    'reviews': (Review, 'review.csv',
                ('id', 'title_id', 'text', 'author_id', 'score', 'pub_date')),
    'comments': (Comment, 'comments.csv',
                 ('id', 'review_id', 'text', 'author_id', 'pub_date')),
}


def import_table(table):
    details = import_dict[table]
    csvfile = 'static/data/' + details[1]
    with open(csvfile, encoding='utf-8') as file:
        rows = csv.reader(file)
        next(rows)
        for row in rows:
            try:
                data = {}
                fields = details[2]
                if details[0].objects.filter(id=row[0]).exists():
                    raise ValueError
                for count, value in enumerate(fields):
                    data[value] = row[count]
                new_record = details[0](**data)
                new_record.save()
            except ValueError:
                print(f'Record details are incorrect or record exists: {row}')
            except IndexError:
                print(f'Record details do not suit table format: {row}')
            except IntegrityError:
                print(f'Integrity error, record was not added: {row}')


class Command(BaseCommand):
    help = 'Add data from .csv file(s)'

    def add_arguments(self, parser):
        parser.add_argument('table', type=str, help='Table name or "all"')

    def handle(self, *args, **kwargs):
        table_name = kwargs['table']
        table_list = []
        if table_name in import_dict:
            table_list.append(table_name)
        if table_name == 'all':
            table_list = import_dict.keys()
        for table in table_list:
            import_table(table)
            self.stdout.write(f'Import finished: {table}')
        if not table_list:
            self.stdout.write(f'Incorrect table name: {table_name}')
