import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo


TIME_ZONES = [
    "UTC",
    "Asia/Karachi",
    "Europe/London",
    "Australia/Sydney",
    "Asia/Tokyo",
    "Europe/Berlin"
]


st.title("Time Zone App")

select_timezone = st.multiselect("Select TimeZones", TIME_ZONES, default=["UTC", "Asia/Karachi"])

st.subheader("Selected Timezones")

for tz in select_timezone:
    current_time = datetime.now(ZoneInfo(tz)).strftime("%Y-%m-%d %I %H:%M:%S %p")

    st.write(f"**{tz}**: {current_time}")

st.subheader("Convert Time Between Timezones")

current_time = st.time_input("Current Time", value=datetime.now().time())

from_tz = st.selectbox("From Timezone", TIME_ZONES, index=0)

to_tz = st.selectbox("To Timezone", TIME_ZONES, index=1)

if st.button("Current Time"):
    dt = datetime.combine(datetime.today(), current_time, tzinfo=ZoneInfo(from_tz))

    converted_time = dt.astimezone(ZoneInfo(to_tz)).strftime("%Y-%m-%d %I %H:%M:%S %p")

    st.success(f"Converted Time {to_tz}: {converted_time}")