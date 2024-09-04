# icalendar: https://icalendar.readthedocs.io/en/latest/about.html
# recurring_ical_event: https://pypi.org/project/recurring-ical-events/

import json
from datetime import datetime, timedelta
from icalendar import Calendar, Event
import os

with open('data.json', 'r') as f:
    courses = json.load(f)

start_date = datetime(2024, 8, 26)
end_time = datetime(2024, 12, 13)
cal = Calendar()

days_map = {
    "Monday": "MO",
    "Tuesday": "TU",
    "Wednesday": "WE",
    "Thursday": "TH",
    "Friday": "FR",
    "Saturday": "SA",
    "Sunday": "SU"
}

for course in courses:
    event = Event()
    event.add('summary', course['title']) 
    event.add('description', course['description'])
    event.add('location', course['location'])
    
    # Parse the course start time
    course_time = datetime.strptime(course['start_time'], '%I:%M %p').time()

    for day in course['days']:
        # Get the weekday number (0 for Monday, 1 for Tuesday, etc.)
        course_day_number = list(days_map.keys()).index(day)

        # Adjust the start_date to the first occurrence of this day
        first_occurrence = start_date
        while first_occurrence.weekday() != course_day_number:
            first_occurrence += timedelta(days=1)

        # Combine the first occurrence date with the course time
        dtstart = datetime.combine(first_occurrence, course_time)

        # Add the start time to the event
        event.add('dtstart', dtstart)

        # Set the recurrence rule (weekly on specified days)
        rrule = {'freq': 'weekly', 'byday': [days_map[d] for d in course['days']]}
        event.add('rrule', rrule)

        # Add the event to the calendar
        cal.add_component(event)

# Write the calendar to a file
directory = '.'
file_path = os.path.join(directory, 'example2.ics')

with open(file_path, 'wb') as f:
    f.write(cal.to_ical())

print(f"ICS file created at: {file_path}")