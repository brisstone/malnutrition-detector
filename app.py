import streamlit as st
import pandas as pd
import joblib

# 1. Load the trained model and encoder we saved earlier
try:
    model = joblib.load('malnutrition_model.pkl')
    encoder = joblib.load('label_encoder.pkl')
except:
    st.error("Model files not found. Please ensure 'malnutrition_model.pkl' and 'label_encoder.pkl' are in the same folder.")
    st.stop()

# 2. Set up the Web Page Design
st.set_page_config(page_title="Child Malnutrition Detector", layout="centered")
st.title("🩺 Malnutrition Early Detection System")
st.write("A pattern recognition decision-support tool for rural health workers.")
st.markdown("---")

# 3. Create the Input Form for Health Workers
st.subheader("Enter Patient Vitals")
col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age (in months)", min_value=6, max_value=59, value=24)
    weight = st.number_input("Weight (kg)", min_value=2.0, max_value=30.0, value=10.0, step=0.1)

with col2:
    height = st.number_input("Height (cm)", min_value=40.0, max_value=130.0, value=80.0, step=0.1)
    muac = st.number_input("MUAC (cm)", min_value=8.0, max_value=20.0, value=13.0, step=0.1)

# 4. Auto-calculate BMI
height_m = height / 100
bmi = weight / (height_m ** 2)
st.info(f"**Auto-Calculated BMI:** {bmi:.2f}")

# 5. Prediction Logic
if st.button("Predict Nutritional Status", type="primary", use_container_width=True):
    
    # Package the inputs into the exact format the model expects
    input_data = pd.DataFrame({
        'age_months': [age],
        'weight_kg': [weight],
        'height_cm': [height],
        'muac_cm': [muac],
        'bmi': [bmi]
    })

    # Run the data through the Logistic Regression model
    pred_encoded = model.predict(input_data)[0]
    
    # Convert the numerical prediction back to text (Severe, Moderate, Normal)
    prediction = encoder.inverse_transform([pred_encoded])[0]

    # Display the final result to the health worker
    st.markdown("---")
    st.subheader("Diagnostic Result:")
    
    if prediction == 'severe':
        st.error("🚨 **SEVERE MALNUTRITION DETECTED** \n\nImmediate clinical intervention required.")
    elif prediction == 'moderate':
        st.warning("⚠️ **MODERATE MALNUTRITION** \n\nNutritional support and close monitoring recommended.")
    else:
        st.success("✅ **NORMAL** \n\nChild's nutritional status is healthy.")
