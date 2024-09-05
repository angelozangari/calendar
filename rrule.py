import json
from datetime import datetime, timedelta
from icalendar import Calendar, Event
import os

# Load course data from JSON file
with open('data.json', 'r') as f:
    courses = json.load(f)

start_date = datetime(2024, 8, 26)  # Start date of the semester
end_date = datetime(2024, 12, 13)   # End date of the semester
cal = Calendar()

# Map days of the week to icalendar format
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
    # Parse the course start and end times
    course_start_time = datetime.strptime(course['start_time'], '%I:%M %p').time()
    course_end_time = datetime.strptime(course['end_time'], '%I:%M %p').time()

    # Create separate events for each day the course is held
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
        dtstart = datetime.combine(first_occurrence, course_start_time)
        dtend = datetime.combine(first_occurrence, course_end_time)

        # Add the start and end time to the event
        event.add('dtstart', dtstart)
        event.add('dtend', dtend)

        # Set the recurrence rule (weekly on specified days)
        rrule = {'freq': 'weekly', 'byday': days_map[day], 'until': end_date}
        event.add('rrule', rrule)

        # Add the event to the calendar
        cal.add_component(event)

# Write the calendar to a file
directory = '.'
file_path = os.path.join(directory, 'example2.ics')

with open(file_path, 'wb') as f:
    f.write(cal.to_ical())

print(f"ICS file created at: {file_path}")
