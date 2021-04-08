from datetime import datetime,date,timedelta
import calendar
current_time = datetime.now()
current_day=current_time.date()


d='2021-04-08'
startdate = list(map(int, d.split('-')))
startevent = date(startdate[0], startdate[1], startdate[2])
first_day = current_day.replace(day = 1)


next_month = current_day.replace(day=28) + timedelta(days=4)
last_day=next_month - timedelta(days=next_month.day)

print(last_day)

if startevent>first_day and startevent<last_day:
	print("yes")
