import streamlit as st

st.title("simple streamlit App")

user_input = st.text_input("Enter Your text")

if st.button("Show Text"):
    st.write(f"you enter: {user_input}")

