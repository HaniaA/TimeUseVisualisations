#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 11:33:36 2019

@author: haniaadamczyk
"""

from person import Person
import datetime as dt

today = dt.datetime.today()
today = today.replace(hour=0,minute=0,second=0,microsecond=0)
week_from_today = today - dt.timedelta(days=7)

main_email = "myemail@gmail.com"
calendar_ids = ["myemail@gmail.com"]

user_instance = Person(main_email,calendar_ids)
user_instance.generate_graphs(week_from_today,today)
