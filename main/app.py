import requests
import streamlit as st
from config import api_key, partner_key


# Get all avaiable car makes for the year
def get_car_makes(year):
    url = f'https://api.carmd.com/v3.0/make?year={year}'
    headers = {
        'content-type': 'application/json',
        'authorization': api_key,
        'partner-token': partner_key
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if 'data' in data:
            return data['data']
        else:
            st.error("No data found for car makes.")
            return []
    else:
        st.error(f"Error: {response.status_code} - {response.json().get('message', 'Unknown error')}")
        return []





# Streamlit UI
st.title("Car Search App")

year = st.text_input("Enter the year:")
car_makes = []

if year:
    try:
        year = int(year)
        car_makes = get_car_makes(year)
    except ValueError:
        st.error("Please enter a valid year.")

if car_makes:
    make = st.selectbox("Select the make:", car_makes)
else:
    make = None

if make:
    st.write(f"You have selected {make} for the year {year}")

