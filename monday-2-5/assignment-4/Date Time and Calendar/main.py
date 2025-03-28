import math,calendar
from datetime import datetime, date, time, timedelta

print("Value of pi:", math.pi)
print("Value of e:", math.e)

print("Square root of 16:", math.sqrt(16))

print("Factorial of 5:", math.factorial(5))

print("2 raised to the power 3:", math.pow(2,3))

print("Natural logarithm of 10:", math.log(10))

print("Logarithm of 1000 with base 10", math.log(1000,10))

angle_red = math.radians(45)

print("Sine of 45 Degrees", math.sin(angle_red))
print("Cosine of 45 Degrees:", math.cos(angle_red))
print("Tangent of 45 Degrees:", math.tan(angle_red))



now = datetime.now()
print("Current date and time:", now)

specific_date = date(2025, 3, 28)
print("Specific date:", specific_date)

specific_time = time(5, 39, 45)
print("Specific time:", specific_time)



formated_date = now.strftime("%Y-%m-%d %H:%M:%S")
print("Formated Date and Time:", formated_date)

date_string = "2025-27-03 05:56:30"
parsed_date = datetime.strptime(date_string, "%Y-%d-%m %H:%M:%S")
print("Parsed date and time:", parsed_date)



print("Current date and time: ", now)

#Add 7 days

future_date = now + timedelta(days=7)
print("Date after 7 days:", future_date)

#Subtract 30 minutes

past_time = now - timedelta(minutes=30)
print("Time 30 minutes ago:", past_time)




year = 2025
month = 3
cal = calendar.TextCalendar()
print(cal.formatmonth(year, month))



yeear = 2024
is_leap = calendar.isleap(yeear)
print(f"Is {yeear} a leap year?", is_leap)