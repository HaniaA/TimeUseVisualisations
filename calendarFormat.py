#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 12:51:33 2019

@author: haniaadamczyk
"""

from dateutil.parser import parse
import datetime as dt
from operator import itemgetter
from nltk.corpus import stopwords
import pandas as pd
import pytz

class CalendarFormat:

    def __init__(self, tCalendar_id):
        self.calendar_id = tCalendar_id
    
    """UTILITY_METHODS"""
    
    def rfc_iso_to_datetime(isodate):
        """Converts isoformat(rfc) into datetime type"""     
        return parse(isodate)
    
    def findListOfEventsFromList(self, date_start, date_end, events_list):
        """filters out events that are in between given dates from the lsit of events"""
        returnList = []
        utc=pytz.UTC#
        date_start = date_start.replace(tzinfo=utc) if(date_start.tzinfo is None or date_start.tzinfo.utcoffset(date_start) is None) else date_start
        date_end = date_end.replace(tzinfo=utc) if(date_end.tzinfo is None or date_end.tzinfo.utcoffset(date_end) is None) else date_end
        
        for eventItem in events_list:
            
            if ('dateTime' in eventItem['start']):
                eventStart = CalendarFormat.rfc_iso_to_datetime(eventItem['start']['dateTime'])
                eventEnd = CalendarFormat.rfc_iso_to_datetime(eventItem['end']['dateTime'])
            else:
                eventStart = dt.datetime.strptime(eventItem['start']['date'], "%Y-%m-%d")
                eventEnd = dt.datetime.strptime(eventItem['end']['date'], "%Y-%m-%d")
                utc=pytz.UTC#
                eventStart = eventStart.replace(tzinfo=utc)#
                eventEnd = eventEnd.replace(tzinfo=utc)#
            
            if ((eventStart<=date_start and eventEnd>date_start) or (eventStart<date_end and eventEnd>=date_end) or (eventEnd<=date_end and eventStart>=date_start)):
                returnList = returnList + [eventItem]
        return returnList
    
    def produce_distribution_of_time_dict(events, no_of_activities=0):
        timeDistribution = {}
        summaries, words = CalendarFormat.produce_summaries_words_distribution(events)

        for event in events:
            try:
                summary_original = event["summary"]
                summary = summary_original.lower()
                word_list = summary.split()
                added_summary=0
                for word_original in word_list:
                    word = word_original.lower()
                    if CalendarFormat.word_valid(word):
                        if words[word]>summaries[summary]:    
                            if word in timeDistribution.keys():
                                timeDistribution[word]+=CalendarFormat.event_duration(event)
                            else:
                                timeDistribution[word]=CalendarFormat.event_duration(event)
                        elif added_summary==0:
                            if summary in timeDistribution.keys():
                                timeDistribution[summary]+=CalendarFormat.event_duration(event)
                            else:
                                timeDistribution[summary]=CalendarFormat.event_duration(event)
                            added_summary=1    
            except KeyError:
                print("No summary KeyError")
        
        timeDistribution = dict((k.upper(), v) for k,v in timeDistribution.items())
        timeDistribution = sorted(timeDistribution.items(), key=itemgetter(1), reverse=True)
        timeDistributionDF = pd.DataFrame(timeDistribution, columns=['Activity', 'Total time'])
        if(no_of_activities!=0):
            timeDistributionDF = timeDistributionDF[:no_of_activities]
        return timeDistributionDF
    
    def produce_distribution_of_time(events, no_of_activities=0, dictionary=False):
        summaries, words = CalendarFormat.produce_summaries_words_distribution(events)
              
        df = pd.DataFrame(columns=['Activity','Activity lower','Total time'])
        
        for event in events:
            try:
                summary_original = event["summary"]
                summary = summary_original.lower()
                word_list = summary_original.split()
                if word_list[0].islower():
                    summary_original.capitalize()
                added_summary=0
                for word_original in word_list:
                    word = word_original.lower()
                    if word_original.islower():
                        word_original = word_original.capitalize()
                    if (CalendarFormat.word_valid(word) and CalendarFormat.event_duration(event)<=132):
                        if words[word]>summaries[summary]:    
                            if word in list(df['Activity lower']):
                                df.at[int(df.index[df['Activity lower'] == word][0]), 'Total time'] += CalendarFormat.event_duration(event)
                            else:
                                df.loc[len(df)]=[word_original,word,CalendarFormat.event_duration(event)]
                        elif added_summary==0:
                            if summary in list(df['Activity lower']):
                                df.at[int(df.index[df['Activity lower'] == summary][0]), 'Total time'] += CalendarFormat.event_duration(event)
                            else:
                                df.loc[len(df)]=[summary_original,summary,CalendarFormat.event_duration(event)]
                            added_summary=1    
            except KeyError:
                print("No summary KeyError")
        
        df = df.sort_values(by=['Total time'], ascending=False)
        del df['Activity lower']
        if no_of_activities!=0:
            df = df[:no_of_activities]
        df["Total time"] = df["Total time"].round(2)
        if dictionary==True:
            df_dict = {}
            for index, row in df.iterrows():
                df_dict[row["Activity"]]=row["Total time"]
            df = df_dict
        return df
    
    def produce_summaries_words_distribution(events):
        summaries = {}
        words = {}
        for event in events:
            try:
                summary = event["summary"]
                summary = summary.lower()
                if summary in summaries.keys():
                    summaries[summary]+=1
                else:
                    summaries[summary]=1
                event_words = event["summary"].split()
                for word in event_words:
                    if CalendarFormat.word_valid(word):
                        word = word.lower()
                        if word in words.keys():
                            words[word]+=1
                        else:
                            words[word]=1
            except KeyError:
                print("No summary KeyError")
        return summaries, words
    
    def produce_distribution_of_time_total(events, no_of_categories):
        summaries, words = CalendarFormat.produce_summaries_words_distribution(events)       
        df = pd.DataFrame(columns=['Activity','Activity lower','Total time'])
        
        for event in events:
            try:
                labels={}
                summary_original = event["summary"]
                summary = summary_original.lower()
                word_list = summary_original.split()
                for word in word_list:
                    if CalendarFormat.word_valid(word):
                        labels[word]=words[word.lower()]
                
                best_word = max(labels.items(), key=itemgetter(1))[0]
                    
                if word_list[0].islower():
                    summary_original.capitalize()
                
                word = best_word.lower()
                if best_word.islower():
                    best_word = best_word.capitalize()

                if CalendarFormat.word_valid(word) and words[word]>summaries[summary]:    
                    if word in list(df['Activity lower']):
                        df.at[int(df.index[df['Activity lower'] == word][0]), 'Total time'] += CalendarFormat.event_duration(event)
                    else:
                        df.loc[len(df)]=[best_word,word,CalendarFormat.event_duration(event)]
                else:
                    if summary in list(df['Activity lower']):
                        df.at[int(df.index[df['Activity lower'] == summary][0]), 'Total time'] += CalendarFormat.event_duration(event)
                    else:
                        df.loc[len(df)]=[summary_original,summary,CalendarFormat.event_duration(event)]
            except KeyError:
                print(event)
                print("No summary KeyError")
            except ValueError:
                print(event)
                print("ValueError: max() arg is an empty sequence")
        
        
        df = df.sort_values(by=['Total time'], ascending=False)
        del df['Activity lower']
        
        df_other = df.iloc[no_of_categories-1:,:]
        df = df[:no_of_categories-1]
        
        other = {"Activity": "Other", "Total time": df_other.sum()["Total time"]}
        
        if(other["Total time"]!=0):
            df = df.append(other, ignore_index=True)

        df = df.sort_values(by=['Total time'], ascending=False)
        df["Total time"] = df["Total time"].round(2)
        
        return df
    
    def produce_distribution_of_time_total_string(events):
        output = ""
        for event in events:
            try:
                summary_original = event["summary"] + " "
                output = output + summary_original * round(CalendarFormat.event_duration(event))
            except KeyError:
                print(event)
                print("No summary KeyError")
        if output is "":
            output="No events this week"
        return output
    
    def most_popular_word(word_list):
        return None
    
    def word_valid(word):
        if (word.lower() not in stopwords.words('english') and any(c.isalpha() for c in word)):
            return True
        else:
            return False
        
    def use_word_instead_summary(word, summary, summaries, words):
        if(summaries[summary]<words[word]):
            return True
        else:
            return False
    
    def events_total_duration(events_list):
        """ function that takes as an argument list of events and returns how much time all those events in total take, 
        measured in hours
    
        Arguments
            events_list (list of events) - list of events of dictionary type, that are imported from google calendar API
        Returns
            accumulator (float) number of hours that the events in total take """

        accumulator=0
        for eventItem in events_list:
            #event,type must be valid as all day events are already filtered out
            duration = CalendarFormat.event_duration(eventItem)
            if (duration<24.0):
                accumulator = accumulator + duration
        return accumulator
    
    def event_duration(event):
        dateTimeItemS = CalendarFormat.rfc_iso_to_datetime(event['start']['dateTime'])
        dateTimeItemE = CalendarFormat.rfc_iso_to_datetime(event['end']['dateTime'])
        duration = (dateTimeItemE - dateTimeItemS).total_seconds()/3600.0
        return duration
 