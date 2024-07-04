import streamlit as st
import pandas as pd
import joblib
import numpy as np

def get_closest_valid_choice(user_input, valid_choices):
    closest_choice = min(valid_choices, key=lambda x: abs(float(x) - float(user_input)))
    return closest_choice

st.title("Sleep Quality Prediction")

# Load your pre-trained model and other necessary objects
model = joblib.load(r"C:\Users\wailb\Desktop\FINAL PROJECT\sleep_quality_predictor\ridge_model.pkl")
label_encoders = joblib.load(r"C:\Users\wailb\Desktop\FINAL PROJECT\sleep_quality_predictor\label_encoders.pkl")
scaler = joblib.load(r"C:\Users\wailb\Desktop\FINAL PROJECT\sleep_quality_predictor\scaler.pkl")
pca = joblib.load(r"C:\Users\wailb\Desktop\FINAL PROJECT\sleep_quality_predictor\pca.pkl")
poly = joblib.load(r"C:\Users\wailb\Desktop\FINAL PROJECT\sleep_quality_predictor\poly.pkl")

# Valid choices for each input
valid_ages = [27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59]
valid_genders = ['Male', 'Female']
valid_occupations = ['Software Engineer', 'Doctor', 'Sales Representative', 'Teacher', 'Nurse', 'Engineer', 'Accountant', 'Scientist', 'Lawyer', 'Salesperson', 'Manager']
valid_sleep_durations = [6.1, 6.2, 5.9, 6.3, 7.8, 6.0, 6.5, 7.6, 7.7, 7.9, 6.4, 7.5, 7.2, 5.8, 6.7, 7.3, 7.4, 7.1, 6.6, 6.9, 8.0, 6.8, 8.1, 8.3, 8.5, 8.4, 8.2]
valid_physical_activities = [i for i in range(0, 101)]
valid_stress_levels = [i for i in range(1, 11)]
valid_bmi_categories = ['Underweight', 'Normal', 'Overweight', 'Obese']
valid_heart_rates = [i for i in range(50, 101)]
valid_daily_steps = [4200, 10000, 3000, 3500, 8000, 4000, 4100, 6800, 5000, 7000, 5500, 5200, 5600, 3300, 4800, 7500, 7300, 6200, 6000, 3700]
valid_sleep_disorders = ['None', 'Sleep Apnea', 'Insomnia']

# Collect user inputs with validation
age = st.slider("How old are you?", 20 , 65, 30)
age = get_closest_valid_choice(age, valid_ages)
gender = st.selectbox("What's your gender?", valid_genders)
occupation = st.selectbox("What's your occupation?", valid_occupations)
sleep_duration = st.slider("How many hours do you sleep per day?", 3, 9, 7)
sleep_duration = get_closest_valid_choice(sleep_duration, valid_sleep_durations)
physical_activity = st.slider("What's your physical activity level? (0-100)", 0, 100, 50)
physical_activity = get_closest_valid_choice(physical_activity, valid_physical_activities)
stress_level = st.slider("What's your stress level? (1-10)", 1, 10, 5)
stress_level = get_closest_valid_choice(stress_level, valid_stress_levels)
bmi_category = st.selectbox("What's your BMI category?", valid_bmi_categories)
heart_rate = st.slider("What's your average heart rate?", 40, 120, 70)
heart_rate = get_closest_valid_choice(heart_rate, valid_heart_rates)
daily_steps = st.slider("How many steps do you take daily?", 1000, 12000, 5000)
daily_steps = get_closest_valid_choice(daily_steps, valid_daily_steps)
sleep_disorder = st.selectbox("Do you have any sleep disorder?", valid_sleep_disorders)

# Button to trigger prediction
if st.button("Predict"):
    # Encode categorical variables
    gender_encoded = np.array([label_encoders['Gender'].transform([gender])[0]]).reshape(1, -1)
    occupation_encoded = np.array([label_encoders['Occupation'].transform([occupation])[0]]).reshape(1, -1)
    bmi_category_encoded = np.array([label_encoders['BMI Category'].transform([bmi_category])[0]]).reshape(1, -1)
    sleep_disorder_encoded = np.array([label_encoders['Sleep Disorder'].transform([sleep_disorder])[0]]).reshape(1, -1)

    # Normalize numerical features
    input_data = scaler.transform([[age, sleep_duration, physical_activity, stress_level, heart_rate, daily_steps]])
    
    # Apply PCA transformation
    input_data_pca = pca.transform(input_data)
    
    # Combine all features
    combined_data = np.hstack([gender_encoded, occupation_encoded, bmi_category_encoded, sleep_disorder_encoded, input_data_pca])
    
    # Generate polynomial features
    input_data_poly = poly.transform(combined_data)

    # Predict sleep quality using the trained Ridge model
    predicted_quality = model.predict(input_data_poly)[0]
    
    st.write(f'Predicted Quality of Sleep: {predicted_quality}')

