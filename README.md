# Automatic Time Recording for Mocoapp

This application automatically records working time when starting and stopping a PC. Additionally, breaks are recorded using the lock screen.

The application also writes a log about the working hours and writes down the values in the application https://www.mocoapp.com/.

This application is not related to mocoapp. It only uses their API.

## CLI Commands


activities --list

start --date --time

stop --date --time

pause-start

pause-stop


fix-pause   --pause-timeslot --minmal-pause


fix-overtime  --day-distribution --ignore


fix-endless-time
