# -*- coding: utf-8 -*-
import re

from datetime import date
import datetime

class date_compare:

    def __init__(self, date_new, period):

        self.date_const = datetime.datetime.now().date()
        self.time_const = datetime.datetime.now().time().strftime("%H:%M")
        self.date_new = date_new
        self.period = period


    def converting(self):
        if len(self.period) >1:
            number = re.findall('\d+', self.period)[0]
            number = int(number)
            if "мин" in self.period:
                d = self.date_new + datetime.timedelta(minutes=number)
                return d
            elif "час" in self.period:
                d = self.date_new + datetime.timedelta(hours=number)
                return d
            elif "ден" in self.period or "сут" in self.period:
                d = self.date_new + datetime.timedelta(days=number)
                return d
            elif "неде" in self.period:
                d = self.date_new + datetime.timedelta(hours=number)
                return d
        else:
            return "1"





    def compare_date(self):
        if self.date_new.date() == self.date_const and self.date_new.time().strftime("%H:%M") == self.time_const:

            new = f"{self.date_const.strftime('%Y-%m-%d')}T{self.time_const}:00"

            return self.converting()
        else:
            return "0"









