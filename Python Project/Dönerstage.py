from __future__ import print_function
import os.path
from re import T
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from datetime import date
from datetime import time
import json

#https://docs.google.com/spreadsheets/d/1a8SvL8yVzjOl-Ff-C1cxygrmraMpQ98STSJ5cT6v28M/edit?usp=sharing

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1a8SvL8yVzjOl-Ff-C1cxygrmraMpQ98STSJ5cT6v28M'


def main():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)
    range_names = [
        'E5:F29',
        'G5:H29',
        'I5:J29',
        'K5:L29',
        'M5:N29',
        'O5:P29',
        'Q5:R29',
        'S5:T29',
        'U5:V29',
        'W5:X29',
        'Y5:Z29'
    ]
    result = service.spreadsheets().values().batchGet(
        spreadsheetId=SPREADSHEET_ID, ranges=range_names, majorDimension='COLUMNS').execute()
    ranges = result.get('valueRanges', [])
    print('{0} ranges retrieved.'.format(len(ranges)))
    day = input('Datum: ')
    counter = 0
    temp = 0
    foundDay = False
    DayColumn = ''
    Zusatz = ''
    for col in ranges:
        for val in col['values']:
            if day in val:
                temp = counter
                foundDay = True
                DayColumn = val
                
            if temp == counter-1 and foundDay:
                foundDay = False
                Zusatz = val
            counter = counter + 1
    print(DayColumn)
    print(Zusatz)
if __name__ == '__main__':
    main()