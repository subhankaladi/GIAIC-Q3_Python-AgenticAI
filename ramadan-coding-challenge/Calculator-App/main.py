import streamlit as st 

st.title("Simple Calculator App")
st.write("Enter your two numbers and choose an operation")

def main():
    col1, col2 = st.columns(2)
    with col1:
        num1 = st.number_input("Enter Your First Number", value=0.0)

    with col2:
        num2 = st.number_input("Enter Your Second Number", value=0.0)

    operations = st.selectbox("Choose operation", ["Addition", "Subtraction", "Multiplication", "Division"])

    if st.button("Calculate"):
        if operations == "Addition":
            result = num1 + num2
            symbol = "+"
        elif operations == "Subtraction":
            result = num1 - num2
            symbol = "-"
        elif operations == "Multiplication":
            result = num1 * num2
            symbol = "*"
        elif operations == "Division":
            if num2 == 0:
                st.error("Error: Division by Zero")
                return
            result = num1 / num2
            symbol = "/"
        
        st.success(f"{num1} {symbol} {num2} = {result}")

if __name__ == "__main__":
    main()
