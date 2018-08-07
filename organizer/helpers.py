from datetime import datetime, timedelta
import time 

def get_dt():
	dt = datetime.now()
	if time.localtime().tm_isdst == 0:
		dt += timedelta(hours=1)
	dt = dt.replace(tzinfo=None)
	return dt