import streamlit as st
import random
import time
import requests

st.title("Money Making Machine")

def generate_money():
    return random.randint(1, 1000)

st.subheader("Instant Cash Generator")
if st.button("Generate Money"):
    st.write("Counting your money....")
    time.sleep(2)
    amount = generate_money()
    st.success(f"You Made ${amount}")


def fetch_side_hustle():
    try:
        response = requests.get("http://127.0.0.1:8000/side_hustles")
        if response.status_code == 200:
            hustles = response.json()
            return hustles["side_hustle"]
        else : 
            print("Freelancing")
    except:
        return ("Something Went Wrong")
    
st.subheader("Side Hustle Ideas")

if st.button("Generate Husple"):
    idea = fetch_side_hustle()
    st.success(idea)

def fetch_money_quote():
    try:
        response = requests.get("http://127.0.0.1:8000/money_quotes")
        if response.status_code == 200:
            quotes =response.json()
            return quotes["money_quote"]
        else:
            return ("Money is the root of al evil")
    except:
        return ("Something went wrong")
st.subheader("Money-Making Motivation")
if st.button("Get Started "):
    quote = fetch_money_quote()
    st.success(quote)