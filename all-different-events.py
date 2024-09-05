import json
from datetime import datetime, timedelta
from icalendar import Calendar, Event
import os

# Load course data from JSON file
with open('data.json', 'r') as f:
    courses = json.load(f)

start_date = datetime(2024, 8, 26)  # Start date of the semester
end_date = datetime(2024, 12, 13)  # End date of the semester

cal = Calendar()

# Map days of the week to weekday numbers
days_map = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6
}

for course in courses:
    # Parse the course start and end times
    course_start_time = datetime.strptime(course['start_time'], '%I:%M %p').time()
    course_end_time = datetime.strptime(course['end_time'], '%I:%M %p').time()

    # Create events for each day the course is held
    for day in course['days']:
        course_day_number = days_map[day]
        current_date = start_date

        while current_date <= end_date:
            if current_date.weekday() == course_day_number:
                event = Event()
                event.add('summary', course['title'])
                event.add('description', course['description'])
                event.add('location', course['location'])

                dtstart = datetime.combine(current_date, course_start_time)
                dtend = datetime.combine(current_date, course_end_time)

                event.add('dtstart', dtstart)
                event.add('dtend', dtend)

                cal.add_component(event)

            current_date += timedelta(days=1)

# Write the calendar to a file
directory = '.'
file_path = os.path.join(directory, 'example3.ics')
with open(file_path, 'wb') as f:
    f.write(cal.to_ical())

print(f"ICS file created at: {file_path}")