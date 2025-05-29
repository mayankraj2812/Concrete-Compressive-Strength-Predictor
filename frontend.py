import streamlit as st
import pickle
import numpy as np
import base64

# Load the model and the scaler
try:
    with open('concrete_strength_model.pkl', 'rb') as file:
        model = pickle.load(file)
    with open('scaler.pkl', 'rb') as file: # Load the scaler
        scaler = pickle.load(file)
    st.sidebar.success("Model and Scaler loaded successfully!")
except FileNotFoundError:
    st.error("Error: Model or scaler file not found. Please run app.ipynb to train and save them.")
    st.stop() # Stop the app if files are not found

# Set background image and white text
def set_background(image_file):
    with open(image_file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        .main-container {{
            background-color: rgba(0, 0, 0, 0.55); /* Dark translucent */
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }}

        html, body, [class*="css"] {{
            color: white !important;
            font-weight: 500;
        }}

        h1, h2, h3, h4, h5, h6 {{
            color: white !important;
        }}

        .stNumberInput label {{
            color: white !important;
        }}

        .stTextInput label {{
            color: white !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Apply background
set_background("background2.jpg")

# Start layout
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align: center;'>Concrete Strength Prediction</h1>", unsafe_allow_html=True)

st.markdown("### Enter the values below to predict compressive strength (MPa):", unsafe_allow_html=True)

# Input fields
cement = st.number_input("Cement (kg/m³)", min_value=0.0, value=300.0)
slag = st.number_input("Blast Furnace Slag (kg/m³)", min_value=0.0, value=0.0)
fly_ash = st.number_input("Fly Ash (kg/m³)", min_value=0.0, value=0.0)
water = st.number_input("Water (kg/m³)", min_value=0.0, value=180.0)
superplasticizer = st.number_input("Superplasticizer (kg/m³)", min_value=0.0, value=0.0)
coarse_agg = st.number_input("Coarse Aggregate (kg/m³)", min_value=0.0, value=900.0)
fine_agg = st.number_input("Fine Aggregate (kg/m³)", min_value=0.0, value=700.0)
age = st.number_input("Age (days)", min_value=1, value=28)

if st.button("Predict Strength"):
    # Create a NumPy array from the input values
    # Ensure the order of features matches the training data
    input_data = np.array([[cement, slag, fly_ash, water, superplasticizer, coarse_agg, fine_agg, age]])

    # Scale the input data using the loaded scaler
    scaled_input_data = scaler.transform(input_data)

    # Make the prediction using the scaled input
    predicted_strength = model.predict(scaled_input_data)[0]

    st.success(f"Predicted Concrete Strength: {predicted_strength:.2f} MPa")

st.markdown('</div>', unsafe_allow_html=True) # Close the main-container div