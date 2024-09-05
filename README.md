Python utility to read course from a json format and parse them into an ics format, that can be then imported on exchange or google calendar.

### Approache
1. **multiple different events** with no reccurent rule: was the one used in all-different-events.py; not scalable because by generating all different events we encounter the following drawbacks:
    - big .ics file
    - slow to import
    - since independent, by eliminating one there's no option to eliminate all future events

2. with **rrules**: winner approach, slim, fast and easy to modify/delete. issue is that importing directly onto apple calendar in an exchange account will mess things up. to fix import it onto a google calendar or directly onto the exchange account from the web interface.

### How to use
Simply add your courses info in the data.json file, which already contains an example.
Change the start and end date of the program in cal-parser.py.
Generate the cal.ics file by running: `python cal-parser.py`