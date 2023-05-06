from datetime import datetime

from django.core.exceptions import ValidationError


def year_not_future(year):
    current_year = datetime.now().year
    if year > current_year:
        raise ValidationError('Year from future is not allowed')
