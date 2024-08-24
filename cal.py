import json
from datetime import datetime, timedelta
from ics import Calendar, Event
from pytz import timezone

with open('data.json', 'r') as f:
    courses = json.load(f)

start_date = datetime(2024, 8, 26)
end_date = datetime(2024, 12, 13)
cal = Calendar()
tz = timezone('America/Chicago')

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
    event.name = course['title']
    event.description = course['description']
    event.location = course['location']

    start_time = datetime.strptime(course['start_time'], "%I:%M %p").time()
    end_time = datetime.strptime(course['end_time'], "%I:%M %p").time()

    course_start_date = next(
        datetime.combine(start_date, start_time) + timedelta(days=i)
        for i in range(7)
        if (start_date + timedelta(days=i)).strftime('%A') in course['days']
    )

    event.begin = tz.localize(course_start_date)
    event.end = tz.localize(course_start_date.replace(hour=end_time.hour, minute=end_time.minute))

    if event.end <= event.begin:
        event.end += timedelta(days=1)

    # ISSUE: ics doesn't support recurring events yet
    # https://icspy.readthedocs.io/en/stable/misc.html#missing-support-for-recurrent-events
    # Events in the iCalendar specification my have a RRULE property that defines a rule or repeating pattern (Todos may have those too). At the moment, ics.py does not have support for either parsing of this property of its usage in the ics.timeline.Timeline class as designing a Pythonic API proved challenging. Support of RRULE is expected to be implemented before version 1.0.

    rrule_days = ','.join([days_map[day] for day in course['days']])
    until_date = tz.localize(end_date.replace(hour=23, minute=59, second=59)).astimezone(timezone('UTC'))
    #event.rrule = f'FREQ=WEEKLY;BYDAY={rrule_days};UNTIL={until_date.strftime("%Y%m%dT%H%M%SZ")}'
    event.created = datetime.now(tz)
    cal.events.add(event)

with open('courses_schedule.ics', 'w') as f:
    f.writelines(cal.serialize())