#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 12:26:25 2019

@author: haniaadamczyk
"""

from importCalendarAPI import CalendarAPI as capi
import datetime as dt
import pytz
from dateutil.parser import parse

class CalendarData:

    """FIELDS and CONSTRUCTOR"""
    service = capi.get_service()

    def __init__(self, tCalendar_ids):
        self.calendar_ids = tCalendar_ids
        
    """UTILITY_METHODS"""
    def rfc_iso_to_datetime(isodate):
        """Converts isoformat(rfc) into datetime type"""
        return parse(isodate)        
    
    def findListOfEventsWithDeleted(self, tStart, tEnd):
        """gets from calendar list of events that are marked cancelled"""
        delta = int((tEnd-tStart).total_seconds()/3600.0/24.0)
        
        tStart_iso = tStart.isoformat() + 'Z'
        tEnd_iso = tEnd.isoformat() + 'Z'   
        
        events = []
        
        for calendar_id in self.calendar_ids:
            try:
                calendar_events = (self.service.events().list(calendarId=(calendar_id),
                                               timeMin=tStart_iso,
                                               timeMax=tEnd_iso,
                                               maxResults=(delta*40),
                                               singleEvents=True,
                                               showDeleted=True,
                                               orderBy='startTime').execute()).get('items',[])
                for event in calendar_events:
                    events.append(event)
            except:
                print("User with calendar id: " + calendar_id + " doesn't exist")
        events = CalendarData.filterOutAllDayEvents(events)
        
        return events
    
    def filterOutAllDayEvents(eventsList):
        """Filter out events, that last whole day"""
        filtered = []
        for eventItem in eventsList:
            if 'dateTime' in eventItem['start']:
                filtered.append(eventItem)
        return filtered
    
    def calendarSnapshot(self, planningTime, firstPlannedDay, lastPlannedDay, filterOutRecurring = False):
        events = self.findListOfEventsWithDeleted(firstPlannedDay, lastPlannedDay)
        plannedevents = []
        planningTime = planningTime.replace(tzinfo=pytz.UTC)
        for event in events:
            try:
                dateTimeCreated = CalendarData.rfc_iso_to_datetime(event['created'])
                dateTimeUpdated = CalendarData.rfc_iso_to_datetime(event['updated'])
                if dateTimeCreated<planningTime:
                    if event['status']=='cancelled':
                        if dateTimeUpdated>planningTime:
                            plannedevents.append(event)
                    else:
                        plannedevents.append(event)
            except ValueError:
                print("ValueError")
                print(event['created'])
                print(event['start']['dateTime'])
            except KeyError:
                print("KeyError")
                print(event['start']['dateTime'])
        if filterOutRecurring == True:
            plannedeventsfinal = CalendarData.filterOutRecurringEvents(plannedevents)
        else:
            plannedeventsfinal = plannedevents
        return plannedeventsfinal
