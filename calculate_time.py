from datetime import datetime, timedelta
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--sdate',default=datetime.today().strftime("%Y-%m-%d"),type=str)
parser.add_argument('--edate',type=str)
parser.add_argument('--day',type=int)
args = parser.parse_args()

def count_mondays(start_date, end_date,day):
    # Convert string dates to datetime objects
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    
    # Ensure the start_date is before end_date
    if start_date > end_date:
        start_date, end_date = end_date, start_date

    # Calculate the number of Mondays
    num_mondays = 0
    current_date = start_date

    while current_date <= end_date:
        if current_date.weekday() == day:  # Monday
            num_mondays += 1
        current_date += timedelta(days=1)

    return num_mondays


def get_day_name_from_int(day_int):
    if 0 <= day_int <= 6:
        # Create a date that is a Monday
        base_date = datetime(2024, 6, 17)  # This is a Monday
        # Calculate the target date by adding the day_int to the base_date
        target_date = base_date + timedelta(days=day_int)
        return target_date.strftime('%A')
    else:
        return "Invalid day number"

start_date = args.sdate
end_date = args.edate
day = args.day
print(f"{count_mondays(start_date, end_date,day)} {get_day_name_from_int(day)}s between {start_date} and {end_date}")
