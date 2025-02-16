from flask import Flask, request, jsonify
import pickle
import numpy as np
import streamlit as st
import pandas

# Load the trained random forest model
pickle_in = open('best_clf.pkl', 'rb')
best_clf = pickle.load(pickle_in)

def main():
    st.set_page_config(page_title="Diabetes Prediction", page_icon="🩺", layout="centered")
    
    # Custom Dark Mode CSS
    st.markdown("""
        <style>
            body {
                background-color: #1E1E1E;
                color: #FFFFFF;
            }
            .main {
                background-color: #1E1E1E;
            }
            h1, h2, h3, h4, h5, h6 {
                color: #FF6F61;
            }
            label {
                color: #D3D3D3;
            }
            .stButton>button {
                background-color: #FF6F61;
                color: white;
                border-radius: 10px;
                width: 100%;
                transition: 0.3s;
            }
            .stButton>button:hover {
                background-color: #FF856F;
            }
            .stSelectbox, .stNumberInput {
                background-color: #2E2E2E;
                color: #FFFFFF;
            }
            .stAlert {
                background-color: #333333;
                border-left: 4px solid #FF6F61;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("🩺 Diabetes Prediction Form")
    st.markdown("""
        <div style="background-color:#FF6F61;padding:15px;border-radius:10px">
        <h2 style="color:white;text-align:center;">Predict Your Risk of Diabetes</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Collect user input
    with st.form(key='diabetes_form'):
        st.subheader("Please provide the following details:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            gender = st.selectbox("Gender:", ["Male", "Female"])
            age = st.number_input("Age:", min_value=1, step=1)
            hypertension = st.selectbox("Hypertension:", ["No", "Yes"])
            heart_disease = st.selectbox("Heart Disease:", ["No", "Yes"])
            
        with col2:
            smoking_history = st.selectbox("Smoking History:", ["Never", "Former", "Current"])
            bmi = st.number_input("BMI:", min_value=0.0, format="%.1f")
            HbA1c_level = st.number_input("HbA1c Level:", min_value=0.0, format="%.1f")
            blood_glucose_level = st.number_input("Blood Glucose Level:", min_value=0)
        
        # Gender Encoding
        gender = 1 if gender == "Male" else 0
        
        # Hypertension Encoding
        hypertension = 1 if hypertension == "Yes" else 0
        
        # Heart Disease Encoding
        heart_disease = 1 if heart_disease == "Yes" else 0
        
        # Smoking History Encoding
        if smoking_history.lower() == "never":
            smoking_history = 4
        elif smoking_history.lower() == "former":
            smoking_history = 3
        elif smoking_history.lower() == "current":
            smoking_history = 1
        
        # Submit Button
        submit_button = st.form_submit_button(label="Submit")
        
        if submit_button:
            # Making Prediction
            input_data = pandas.DataFrame({
                "gender": [gender],
                "age": [age],
                "hypertension": [hypertension],
                "heart_disease": [heart_disease],
                "smoking_history": [smoking_history],
                "bmi": [bmi],
                "HbA1c_level": [HbA1c_level],
                "blood_glucose_level": [blood_glucose_level]
            })
            
            result = best_clf.predict(input_data)
            if result == 0:
                result_text = "No"
                st.success(f"Prediction: You are unlikely to have diabetes. ({result_text})")
            else:
                result_text = "Yes"
                st.error(f"Prediction: You may be at risk of diabetes. ({result_text})")
            
            st.info("Disclaimer: This prediction is based on statistical modeling and should not be considered medical advice. Please consult a healthcare professional for accurate diagnosis.")
            
if __name__ == '__main__':
    main()


