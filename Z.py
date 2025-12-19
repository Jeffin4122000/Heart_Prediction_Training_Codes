import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
import random

# Load the trained model
model = load_model(r'C:\Users\ann_model.h5')

# Initialize session state variables
if 'page' not in st.session_state:
    st.session_state.page = 1

def validate_patient_details():
    if all([
        st.session_state.uhid,
        st.session_state.name,
        st.session_state.height > 0,
        st.session_state.weight > 0,
        st.session_state.age > 0,
        st.session_state.gender
    ]):
        # Store the computed gender as a numeric value in session state
        st.session_state.sex = 1 if st.session_state.gender == "Male" else 0
        st.session_state.page = 2
    else:
        st.warning("Please fill out all required patient details before proceeding.")

# Function to make predictions
def predict_risk(features):
    # Convert features to a NumPy array
    features = np.array(features).reshape(1, -1)
    # Make prediction
    prediction = model.predict(features)
    return prediction[0][0]

st.title("Heart Risk Analyser")

if st.session_state.page == 1:
    st.subheader("Patient Details")

    # Generate a unique identifier for the patient
    st.session_state.uhid = hex(random.randint(0, 2**32-1))
    st.session_state.name = st.text_input("Name")
    st.session_state.height = st.number_input("Height (cm)", min_value=0)
    st.session_state.weight = st.number_input("Weight (kg)", min_value=0)
    st.session_state.age = st.number_input("Age", min_value=0)
    st.session_state.gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    st.session_state.present_complaints = st.text_area("Patient Complaints (optional)")
    
    if st.button("Next"):
        validate_patient_details()

elif st.session_state.page == 2:
    # Get additional risk factor inputs
    calcification_score = st.number_input("Calcification Score", min_value=0, max_value=1000, value=0)
    rf1 = st.selectbox("RF1 (Family History)", ("No", "Yes"))
    rf2 = st.selectbox("RF2 (Smoking)", ("No", "Yes"))
    rf3 = st.selectbox("RF3 (Hypertension)", ("No", "Yes"))
    rf4 = st.selectbox("RF4 (Dyslipidemia)", ("No", "Yes"))
    rf5 = st.number_input("RF5 (Fasting Glucose)", min_value=0.0, max_value=300.0, value=100.0)
    rf6 = st.selectbox("RF6 (Obesity)", ("No", "Yes"))
    rf7 = st.selectbox("RF7 (Lifestyle)", ("Sedentary", "Active"))
    rf8 = st.selectbox("RF8 (CABG)", ("No", "Yes"))
    rf9 = st.selectbox("RF9 (High Serum)", ("No", "Yes"))

    # Convert categorical inputs to numerical values
    rf1 = 1 if rf1 == "Yes" else 0
    rf2 = 1 if rf2 == "Yes" else 0
    rf3 = 1 if rf3 == "Yes" else 0
    rf4 = 1 if rf4 == "Yes" else 0
    rf6 = 1 if rf6 == "Yes" else 0
    rf7 = 1 if rf7 == "Active" else 0
    rf8 = 1 if rf8 == "Yes" else 0
    rf9 = 1 if rf9 == "Yes" else 0

    # Make prediction when button is clicked
    if st.button("Predict Heart Risk"):
        features = [
            st.session_state.age, st.session_state.sex, calcification_score, rf1, rf2, rf3, rf4, rf5, rf6, rf7, rf8, rf9
        ]
        risk_score = predict_risk(features)
        if risk_score > 0.8:
            st.warning(f"The predicted heart risk is high with a score of {risk_score:.2f}")
        elif 0.5< risk_score < 0.8:
            st.warning(f"The predicted heart risk is moderate with a score of {risk_score:.2f}")
        else:
            st.success(f"The predicted heart risk is low with a score of {risk_score:.2f}")
