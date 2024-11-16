from datetime import datetime

Holidays = [
    "01-01",  
    "04-21",  
    "05-01",  
    "09-07",  
    "10-12",  
    "11-02",  
    "11-15",   
    "12-25" 
]

def is_holiday(date):
    today = datetime.now()
    today_str = today.strftime("%m-%d")
    return today_str in Holidays

def is_weekend(date):
    today = datetime.now()
    return today.weekday() >= 5

def is_friday(date):
    today = datetime.now()
    return today.weekday() == 4

if __name__ == "__main__":
    today = datetime.now()
    if is_holiday(today):
        print("Deploy Blocked, Today is a holiday.")
        exit(1)
    elif is_weekend(today):
        print("Deploy Blocked, Today is a weekend.")
        exit(1)
    elif is_friday(today):
        print("Deploy Blocked, Today is Friday.")
        exit(1)
    else:
        print("Deploy Allowed.")
        exit(0)