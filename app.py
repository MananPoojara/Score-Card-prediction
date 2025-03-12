import streamlit as st
import pickle
import pandas as pd
import numpy as np
import time
import streamlit.components.v1 as components

# Function to load model dynamically
@st.cache_resource  # Prevents reloading every time
def load_model(model_name):
    if model_name == "Random Forest":
        return pickle.load(open('rf_pipe.pkl', 'rb'))
    else:
        return pickle.load(open('xgb_pipe.pkl', 'rb'))

st.set_page_config(page_title="🏏Cricket Score Predictor", layout="centered")
st.title("🏏 Cricket Score Predictor")
model_choice = st.radio("🔄 Select Model", ["Random Forest", "XGBoost"])

# Load selected model (only one at a time)
pipe = load_model(model_choice)

teams = sorted([
    'Australia', 'India', 'Bangladesh', 'New Zealand', 'South Africa',
    'England', 'West Indies', 'Afghanistan', 'Pakistan', 'Sri Lanka'
])

cities = sorted([
    'Colombo', 'Mirpur', 'Johannesburg', 'Dubai', 'Auckland', 'Cape Town',
    'London', 'Pallekele', 'Barbados', 'Sydney', 'Melbourne', 'Durban',
    'St Lucia', 'Wellington', 'Lauderhill', 'Hamilton', 'Centurion',
    'Manchester', 'Abu Dhabi', 'Mumbai', 'Nottingham', 'Southampton',
    'Mount Maunganui', 'Chittagong', 'Kolkata', 'Lahore', 'Delhi', 'Nagpur',
    'Chandigarh', 'Adelaide', 'Bangalore', 'St Kitts', 'Cardiff', 'Christchurch',
    'Trinidad'
])
batting_team = st.selectbox("🏏 Select Batting Team", teams)
bowling_team = st.selectbox("🎯 Select Bowling Team", teams)
city = st.selectbox("📍 Match City", cities)
current_score = st.number_input("📊 Current Score", min_value=0, step=1)
overs = st.number_input("⏳ Overs Completed (Min 5)", min_value=5, max_value=20, step=0)
wickets = st.number_input("❌ Wickets Fallen", min_value=0, max_value=10, step=1)
last_five = st.number_input("⚡ Runs in Last 5 Overs", min_value=0, step=1)

# Predict Button
if st.button("🔮 Predict Score"):
    with st.spinner("Predicting... ⏳"):
        time.sleep(3) 

    balls_left = 120 - (overs * 6)
    wickets_left = 10 - wickets
    crr = current_score / overs

    input_df = pd.DataFrame({
        'batting_team': [batting_team],
        'bowling_team': [bowling_team],
        'city': [city],
        'current_score': [current_score],
        'balls_left': [balls_left],
        'wickets_left': [wickets_left],
        'crr': [crr],
        'last_five': [last_five]
    })

    result = pipe.predict(input_df)
    predicted_score = int(result[0])

    st.success(f"🏆 **Predicted Score: {predicted_score}** using **{model_choice}**")
