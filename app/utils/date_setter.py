import datetime
from settings.settings import settings
import random

class DateSetter:

    start_date_string = f'01{settings.date.m}{settings.date.y}'
    start = datetime.datetime.strptime(
        start_date_string, 
        "%d%m%Y"
    ).date()
    end = start + datetime.timedelta(days=29)

    @classmethod
    def get_dates(cls):
        dates = [
            cls.get_randdate() for i in range(8)
        ]
        return dates

    @classmethod
    def get_randdate(cls):
        random_date = cls.start + (cls.end - cls.start) * random.random()
        return random_date