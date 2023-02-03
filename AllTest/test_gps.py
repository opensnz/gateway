import time

timestamp_06_jan_1980 = int(time.mktime(time.strptime("06 Jan 1980", "%d %b %Y")))
gps_start = 315964800
current_timestamp = time.time()

milliseconds = (current_timestamp - timestamp_06_jan_1980) * 1000
print(timestamp_06_jan_1980, gps_start, timestamp_06_jan_1980==gps_start)
print(int(milliseconds))
