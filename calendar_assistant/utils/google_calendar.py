"""Google Calendar API integration."""

import os
import pickle
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pytz

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


class GoogleCalendarClient:
    """Client for Google Calendar API operations."""

    def __init__(self, credentials_file: str = 'credentials.json', token_file: str = 'token.pickle'):
        """Initialize the Google Calendar client.

        Args:
            credentials_file: Path to OAuth2 credentials JSON file
            token_file: Path to store the access token
        """
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.service = None
        self._authenticate()

    def _authenticate(self):
        """Authenticate with Google Calendar API."""
        creds = None

        # Token file stores the user's access and refresh tokens
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                creds = pickle.load(token)

        # If no valid credentials, let user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_file):
                    raise FileNotFoundError(
                        f"Credentials file not found: {self.credentials_file}\n"
                        f"Download it from Google Cloud Console:\n"
                        f"https://console.cloud.google.com/apis/credentials"
                    )
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open(self.token_file, 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('calendar', 'v3', credentials=creds)

    def list_events(
        self,
        max_results: int = 10,
        time_min: Optional[datetime] = None,
        time_max: Optional[datetime] = None,
        calendar_id: str = 'primary'
    ) -> List[Dict[str, Any]]:
        """List upcoming events.

        Args:
            max_results: Maximum number of events to return
            time_min: Start time (defaults to now)
            time_max: End time (defaults to 1 week from now)
            calendar_id: Calendar ID (default: primary)

        Returns:
            List of event dictionaries
        """
        try:
            if time_min is None:
                time_min = datetime.utcnow()

            if time_max is None:
                time_max = time_min + timedelta(days=7)

            events_result = self.service.events().list(
                calendarId=calendar_id,
                timeMin=time_min.isoformat() + 'Z',
                timeMax=time_max.isoformat() + 'Z',
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()

            events = events_result.get('items', [])
            return events

        except HttpError as error:
            print(f'An error occurred: {error}')
            return []

    def get_today_events(self, calendar_id: str = 'primary') -> List[Dict[str, Any]]:
        """Get all events for today.

        Args:
            calendar_id: Calendar ID (default: primary)

        Returns:
            List of today's events
        """
        now = datetime.utcnow()
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)

        return self.list_events(
            max_results=50,
            time_min=start_of_day,
            time_max=end_of_day,
            calendar_id=calendar_id
        )

    def create_event(
        self,
        summary: str,
        start_time: datetime,
        end_time: datetime,
        description: str = '',
        location: str = '',
        attendees: List[str] = None,
        calendar_id: str = 'primary',
        timezone: str = 'UTC'
    ) -> Dict[str, Any]:
        """Create a new calendar event.

        Args:
            summary: Event title
            start_time: Event start time
            end_time: Event end time
            description: Event description
            location: Event location
            attendees: List of attendee emails
            calendar_id: Calendar ID (default: primary)
            timezone: Timezone (default: UTC)

        Returns:
            Created event dictionary
        """
        try:
            event = {
                'summary': summary,
                'location': location,
                'description': description,
                'start': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': timezone,
                },
                'end': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': timezone,
                },
            }

            if attendees:
                event['attendees'] = [{'email': email} for email in attendees]

            created_event = self.service.events().insert(
                calendarId=calendar_id,
                body=event
            ).execute()

            return created_event

        except HttpError as error:
            print(f'An error occurred: {error}')
            return {}

    def update_event(
        self,
        event_id: str,
        summary: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        description: Optional[str] = None,
        calendar_id: str = 'primary',
        timezone: str = 'UTC'
    ) -> Dict[str, Any]:
        """Update an existing event.

        Args:
            event_id: ID of the event to update
            summary: New event title
            start_time: New start time
            end_time: New end time
            description: New description
            calendar_id: Calendar ID (default: primary)
            timezone: Timezone (default: UTC)

        Returns:
            Updated event dictionary
        """
        try:
            # Get current event
            event = self.service.events().get(
                calendarId=calendar_id,
                eventId=event_id
            ).execute()

            # Update fields
            if summary:
                event['summary'] = summary
            if description:
                event['description'] = description
            if start_time:
                event['start'] = {
                    'dateTime': start_time.isoformat(),
                    'timeZone': timezone,
                }
            if end_time:
                event['end'] = {
                    'dateTime': end_time.isoformat(),
                    'timeZone': timezone,
                }

            updated_event = self.service.events().update(
                calendarId=calendar_id,
                eventId=event_id,
                body=event
            ).execute()

            return updated_event

        except HttpError as error:
            print(f'An error occurred: {error}')
            return {}

    def delete_event(self, event_id: str, calendar_id: str = 'primary') -> bool:
        """Delete an event.

        Args:
            event_id: ID of the event to delete
            calendar_id: Calendar ID (default: primary)

        Returns:
            True if successful, False otherwise
        """
        try:
            self.service.events().delete(
                calendarId=calendar_id,
                eventId=event_id
            ).execute()
            return True

        except HttpError as error:
            print(f'An error occurred: {error}')
            return False

    def search_events(
        self,
        query: str,
        max_results: int = 10,
        calendar_id: str = 'primary'
    ) -> List[Dict[str, Any]]:
        """Search for events by keyword.

        Args:
            query: Search query
            max_results: Maximum results to return
            calendar_id: Calendar ID (default: primary)

        Returns:
            List of matching events
        """
        try:
            events_result = self.service.events().list(
                calendarId=calendar_id,
                q=query,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()

            return events_result.get('items', [])

        except HttpError as error:
            print(f'An error occurred: {error}')
            return []

    def get_free_busy(
        self,
        time_min: datetime,
        time_max: datetime,
        calendars: List[str] = None
    ) -> Dict[str, Any]:
        """Check free/busy status.

        Args:
            time_min: Start time
            time_max: End time
            calendars: List of calendar IDs (default: primary)

        Returns:
            Free/busy information
        """
        if calendars is None:
            calendars = ['primary']

        try:
            body = {
                'timeMin': time_min.isoformat() + 'Z',
                'timeMax': time_max.isoformat() + 'Z',
                'items': [{'id': cal_id} for cal_id in calendars]
            }

            result = self.service.freebusy().query(body=body).execute()
            return result

        except HttpError as error:
            print(f'An error occurred: {error}')
            return {}
