from datetime import datetime
import pytz


OTHER_TIMEZONES = [
    pytz.timezone('America/Indiana/Indianapolis'),
    pytz.timezone('America/New_York'),
    pytz.timezone('America/St_Thomas'),
    pytz.timezone('UTC'),
    pytz.timezone('Europe/London'),
    pytz.timezone('Europe/Paris'),
    pytz.timezone('Europe/Vatican'),
    pytz.timezone('Europe/Berlin'),
    pytz.timezone('Europe/Copenhagen'),
    pytz.timezone('Africa/Johannesburg'),
    pytz.timezone('Europe/Moscow'),
    pytz.timezone('Asia/Kolkata'),
    pytz.timezone('Asia/Dubai'),
    pytz.timezone('Asia/Taipei'),
    pytz.timezone('Asia/Shanghai'),
    pytz.timezone('Asia/Hong_Kong'),
    pytz.timezone('Asia/Tokyo'),
    pytz.timezone('Pacific/Honolulu'),
    pytz.timezone('America/Anchorage'),
    pytz.timezone('America/Los_Angeles'),
    pytz.timezone('America/Denver'),
    pytz.timezone('America/Chicago')
]


fmt = '%c %Z UTC%z'


while True:
    date_input = input("When is your meeting?  Please use MM/DD/YYYY HH:MM format. ")
    try:
        local_date = datetime.strptime(date_input, '%m/%d/%Y %H:%M')
    except ValueError:
        print("{} doesn't seem to be a valid date & time.".format(date_input))
    else:
        local_date = pytz.timezone('America/Kentucky/Louisville').localize(local_date)
        utc_date = local_date.astimezone(pytz.utc)

        output = []
        for timezone in OTHER_TIMEZONES:
            output.append(utc_date.astimezone(timezone))
        for appointment in output:
            print(appointment.strftime(fmt))
        break
