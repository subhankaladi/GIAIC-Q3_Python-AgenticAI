import streamlit as st


def convert_units(value, from_unit, to_unit):
    conversion_factors = {
        "meters_kilometers" : 0.001,
        "kilometers_meters": 1000,
        "grams_kilograms" : 0.001,
        "kilograms_grams" : 1000
    }

    key = f"{from_unit}_{to_unit}"

    if key in conversion_factors:
        conversion_factor = conversion_factors[key]
        return value * conversion_factor
    elif conversion_factors == conversion_factors:
        return f"Conversion between {from_unit} and {to_unit} is not possible. Please choose different units."
    else:
        return "Conversion not possible"
    
st.set_page_config(page_title="Unit Converter")
st.title("Unit Converter")

value = st.number_input("Enter the value you want to convert", min_value=1.0, step=1.0)
from_unit = st.selectbox("From", ["meters", "kilometers", "kilograms", "grams"])
to_unit = st.selectbox("To", ["meters", "kilometers", "grams", "kilograms"])

if st.button("Convert"):
    result = convert_units(value, from_unit, to_unit)
    st.write(result)