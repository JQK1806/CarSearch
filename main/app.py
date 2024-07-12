import requests
import streamlit as st
from config import api_key, partner_key


headers = {
        'content-type': 'application/json',
        'authorization': api_key,
        'partner-token': partner_key
    }

# Get all avaiable car makes for the given year
def get_car_makes(year):
    url = f'https://api.carmd.com/v3.0/make?year={year}'
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
    
# Get all avaiable car models for the given make and year
def get_car_models(year, make):
    url = f'https://api.carmd.com/v3.0/model?year={year}&make={make}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if 'data' in data:
            return data['data']
        else:
            st.error("No data found for car models.")
            return []
    else:
        st.error(f"Error: {response.status_code} - {response.json().get('message', 'Unknown error')}")
        return []
    
# Get the avaiable engine information about the given year, make, and model of the car
def get_car_engine(year, make, model):
    url = f'http://api.carmd.com/v3.0/engine?year={year}&make={make}&model={model}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if 'data' in data:
            return data['data']
        else:
            st.error("No data found for engine data.")
            return None
    else:
        st.error(f"Error: {response.status_code} - {response.json().get('message', 'Unknown error')}")
        return None



# Streamlit UI
st.title("Car Search App")

year = st.text_input("Enter the year:")
car_makes = []
car_models = []

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
    car_models = get_car_models(year, make)
    if car_models:
        model = st.selectbox("Select the model:", car_models)
    else:
        model = None

if year and make and model:
    engine_data = get_car_engine(year, make, model)
    if engine_data:
        st.write(f"Engine data for {year}, {make}, {model}.")
        st.json(engine_data)
    else:
        st.write("No engine data found.")