# import
import json
from datetime import datetime, timedelta
from icalendar import Calendar, Event
import os
import pytz

# read json
with open('data.json', 'r') as f:
    courses = json.load(f)

# global vars
tz = pytz.timezone('America/Chicago')
start_date = datetime(2024, 8, 26) # Start date of the semester
end_date = datetime(2024, 12, 13)  # End date of the semester
cal = Calendar() 

days_map = { # Map days of the week to icalendar format
    "Monday": "MO",
    "Tuesday": "TU",
    "Wednesday": "WE",
    "Thursday": "TH",
    "Friday": "FR",
    "Saturday": "SA",
    "Sunday": "SU"
}

# generate ical
for course in courses:
    # Parse the course start and end times
    course_start_time = datetime.strptime(course['start_time'], '%I:%M %p').time()
    course_end_time = datetime.strptime(course['end_time'], '%I:%M %p').time()
    
    # Create different events for each day of the week the course is held
    for day in course['days']:
        event = Event()
        event.add('summary', course['title'])
        event.add('description', course['description'])
        event.add('location', course['location'])

        # Get the weekday number (0 for Monday, 1 for Tuesday, etc.)
        course_day_number = list(days_map.keys()).index(day)

        # Adjust the start_date to the first occurrence of this day
        first_occurrence = start_date
        while first_occurrence.weekday() != course_day_number:
            first_occurrence += timedelta(days=1)

        # Combine the first occurrence date with the course start and end times
        dtstart = tz.localize(datetime.combine(first_occurrence, course_start_time))
        dtend = tz.localize(datetime.combine(first_occurrence, course_end_time))

        # Add the start and end time to the event
        event.add('dtstart', dtstart)
        event.add('dtend', dtend)

        # Set the recurrence rule (weekly on specified days)
        rrule = {'freq': 'weekly', 'byday': days_map[day], 'until': end_date}
        event.add('rrule', rrule)

        # Add the event to the calendar
        cal.add_component(event)

# write ics
directory = '.'
file_path = os.path.join(directory, 'cal.ics')

with open(file_path, 'wb') as f:
    f.write(cal.to_ical())

print(f"ICS file created at: {file_path}")