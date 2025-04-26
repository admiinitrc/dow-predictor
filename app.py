import streamlit as st
import time
import numpy as np

# Page config
st.set_page_config(page_title="Dowry Calculator", page_icon="💍", layout="centered")

# Custom CSS for colors and fonts
st.markdown("""
    <style>
    body {
        background-color: #fff8f0;
    }
    .stTextInput > div > div > input {
        border: 1px solid #f0c27b;
        border-radius: 8px;
    }
    .stSelectbox > div > div {
        border: 1px solid #f0c27b;
        border-radius: 8px;
    }
    .stSlider > div > div > div {
        background: linear-gradient(to right, #f0c27b, #f5af19);
    }
    .stButton > button {
        color: white;
        background: linear-gradient(to right, #f0c27b, #f5af19);
        border: none;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("💍 Indian Dowry Prediction Calculator")
st.write("---")

# Form inputs
with st.form("dowry_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.slider("Age", 21, 40, 25)
        profession = st.selectbox("Profession", ["Engineer", "Doctor", "Lawyer", "Government Job", "Businessman", "Other"])
        subprofession = st.text_input("Sub-Profession (Optional)", placeholder="e.g., Software Engineer, Surgeon")
        highest_education = st.selectbox("Highest Education", ["PhD", "Postgraduate", "Graduate", "Diploma", "Other"])
        college_tier = st.selectbox("College Tier", ["Tier 1", "Tier 2", "Tier 3", "No College"])
        location = st.selectbox("Location", ["Urban", "Semi-Urban", "Rural"])

    with col2:
        monthly_salary = st.number_input("Current Monthly Salary (₹)", min_value=0, step=1000)
        vehicle_ownership = st.selectbox("Vehicle Ownership", ["None", "2-wheeler", "4-wheeler", "Luxury Car"])
        investments = st.number_input("Total Investments (₹)", min_value=0, step=10000)
        pending_loan = st.number_input("Pending Loan Amount (₹)", min_value=0, step=10000)
        property_worth = st.number_input("Property Worth (₹)", min_value=0, step=10000)
        number_of_dependents = st.slider("Number of Dependents", 0, 5, 0)
    
    submitted = st.form_submit_button("Predict Dowry Amount 💰")

# Prediction function (Mathematical model)
def calculate_dowry():
    base = 2_00_000  # 2 lakh minimum
    score = 0
    
    score += (35 - age) * 5
    score += 3 if profession != "Other" else 1
    score += 1 if subprofession else 0
    score += {"PhD": 12, "Postgraduate": 9, "Graduate": 7, "Diploma": 5, "Other": 3}[highest_education]
    score += {"Tier 1": 3, "Tier 2": 2, "Tier 3": 1, "No College": 0}[college_tier]
    score += 5 * (np.log1p(monthly_salary) / 10)
    score += 5 if vehicle_ownership != "None" else 0
    score += 4 * (np.log1p(investments) / 12)
    score += 4 if location == "Urban" else (2 if location == "Semi-Urban" else 1)
    score -= 4 * (np.log1p(pending_loan) / 10)
    score += 6 * (np.log1p(property_worth) / 12)
    score -= number_of_dependents * 6

    dowry = base + (score * 1_00_000)
    dowry = np.clip(dowry, 2_00_000, 2_00_00_000)  # between 2 lakh and 2 crore
    return dowry

# Show prediction
if submitted:
    with st.spinner('Calculating best dowry amount... 💭'):
        time.sleep(2)
        result = calculate_dowry()
        st.success(f"🎉 Predicted Dowry Amount: ₹ {int(result):,}")
