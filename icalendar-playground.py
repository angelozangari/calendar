from datetime import datetime
from icalendar import Calendar, Event
import tempfile, os

cal = Calendar()
event = Event()
event.add('summary', 'lezione di tacos')  # Corrected: 'summary' instead of 'name'
event.add('dtstart', datetime(2024, 9, 1, 12, 12, 12))  # Corrected: 'dtstart' instead of 'dstart'
event.add('rrule', {'freq': 'daily'})
cal.add_component(event)

directory = '.'
file_path = os.path.join(directory, 'example.ics')

with open(file_path, 'wb') as f:
    f.write(cal.to_ical())

print(f"ICS file created at: {file_path}")
