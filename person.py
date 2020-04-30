#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 12:22:12 2019

@author: haniaadamczyk
"""

from calendarData import CalendarData as calData
from calendarFormat import CalendarFormat as calFormat
from visualisation import Visualisation as vis
import datetime as dt
import pandas as pd

class Person:
    """FIELDS and CONSTRUCTOR"""    
    def __init__(self, tEmail, tCalendar_ids):
        self.email = tEmail
        self.calendar_ids = tCalendar_ids
        self.CalendarData = calData(tCalendar_ids)
        self.CalendarFormat = calFormat(tCalendar_ids[0])
        self.Visualisation = vis(tEmail)

    def get_data(self, start_date, end_date):
        data = self.CalendarData.calendarSnapshot(dt.datetime.now(), start_date, end_date)
        return data

    def generate_graphs(self, start_date, end_date):
        names = []
        data = self.get_data(start_date, end_date)

        #Generate time distribution table
        time_dist = calFormat.produce_distribution_of_time(data,10)
        names.append(self.Visualisation.timeDistributionTable(time_dist, start_date, end_date))
        
        #Generate word cloud
        text = calFormat.produce_distribution_of_time_total_string(data)
        names.append(self.Visualisation.total_time_distribution_word_cloud(text, start_date, end_date))
        
        #Generate pie chart
        time_dist_total = calFormat.produce_distribution_of_time_total(data, 10)
        names.append(self.Visualisation.total_time_distribution_pie_chart(time_dist_total, start_date, end_date))
        
        return names
    
    def events_to_csv(events):
        formatted_events = []
        for event in events:
            formatted_event = {}
            for event_key, event_value in event.items():
                if (type(event_value) is dict):
                    for dict_key, dict_value in event_value.items():
                        formatted_event[event_key + "_" + dict_key] = dict_value
                else:
                    formatted_event[event_key] = event_value
            formatted_events.append(formatted_event)
               
        events_df = pd.DataFrame(formatted_events)
        events_df.to_csv('events.csv')
                            
        return formatted_events
    
                    
                
                
            
        
        
        
        
        
    
    