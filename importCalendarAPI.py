#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 11:23:47 2019

@author: haniaadamczyk
"""

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class CalendarAPI:
    
    def __init__(self):
        return
    

    """METHODS"""
    # Setup the Calendar API and get credentials    
    def get_service():
        SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'

        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('credentials/token.pickle'):
            with open('credentials/token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('credentials/token.pickle', 'wb') as token:
                pickle.dump(creds, token)
    
        service = build('calendar', 'v3', credentials=creds)
        
        return service
    
    def retrieve_all_calendars(self):
        page_token = None
        calendar_ids = []
        service = CalendarAPI.get_service()
        while True:
            calendar_list = service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                calendar_ids.append((calendar_list_entry['id'], calendar_list_entry['summary']))
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break
        return calendar_ids



