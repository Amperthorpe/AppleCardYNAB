from datetime import datetime, timedelta

# Get the current date and time
now = datetime.now()

# Calculate the number of days since the last Wednesday
days_since_wednesday = ((now.weekday() + 1) - 3) % 7

print(days_since_wednesday)
