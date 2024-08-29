import datetime

def get_start_and_end_date():
    current_date = datetime.datetime.now()
    last_day_prev_month = current_date.replace(day=1) - datetime.timedelta(days=1)
    start_date = last_day_prev_month.replace(day=1).strftime('%Y-%m-%d')
    end_date = last_day_prev_month.strftime('%Y-%m-%d')

    return {"start_date": start_date, "end_date": end_date}
