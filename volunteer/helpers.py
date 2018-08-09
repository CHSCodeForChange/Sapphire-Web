from datetime import datetime, timedelta
import time 
import pytz

def get_dt():
	dt = datetime.now(pytz.timezone('US/Eastern'))
	if time.localtime().tm_isdst == 0:
		dt += timedelta(hours=1)
	dt = dt
	return dt