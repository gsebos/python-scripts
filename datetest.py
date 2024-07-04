from datetime import datetime, timedelta

def get_day_name_from_int(day_int):
    if 0 <= day_int <= 6:
        # Create a date that is a Monday
        base_date = datetime(2024, 6, 17)  # This is a Monday
        # Calculate the target date by adding the day_int to the base_date
        target_date = base_date + timedelta(days=day_int)
        return target_date.strftime('%A')
    else:
        return "Invalid day number"

print(get_day_name_from_int(5))