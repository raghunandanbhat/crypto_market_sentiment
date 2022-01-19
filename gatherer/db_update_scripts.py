import datetime

date = date = datetime.datetime.today().replace(hour=00, minute=00, second=00, microsecond=000000)

start = date - datetime.timedelta(days=1)#datetime.datetime(2021, 12, 6, 00, 00, 00)
end = date #datetime.datetime(2021, 12, 7, 00, 00, 00)

print(start)
print(end)