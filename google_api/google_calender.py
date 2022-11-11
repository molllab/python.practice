# 0.
# 구글 api 캘린더 열어놓고 > credentials.json 받기
# https://data-newbie.tistory.com/832
# https://velog.io/@kho5420/Python-%EA%B5%AC%EA%B8%80-Open-API%EB%A1%9C-%EC%BA%98%EB%A6%B0%EB%8D%94-%ED%99%9C%EC%9A%A9%ED%95%B4%EB%B3%B4%EA%B8%B0
# https://github.com/sungreong/PyKorAnniversary
# https://idjung.wordpress.com/2021/07/30/google-calendar-api-%EC%9D%B4%EC%9A%A9%ED%95%98%EA%B8%B0-2-3-python-%EC%98%88%EC%A0%9C/

# 1.
# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

# 2.
# https://developers.google.com/calendar/api/quickstart/python
from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()