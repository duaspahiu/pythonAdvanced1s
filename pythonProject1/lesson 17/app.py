
import streamlit as st

st.set_page_config(
    page_title="BMI Calculator",
    page_icon="⚖️",
    layout="centered"
)

# Dark theme styling
st.markdown("""
<style>
.stApp {
    background-color: #0e1117;
    color: #f5f5f5;
}
.block-container {
    max-width: 600px;
    padding-top: 4rem;
}
.stButton button {
    color: #ff4b4b;
    background-color: transparent;
    border: 1px solid #ff4b4b;
    border-radius: 6px;
}
.stButton button:hover {
    background-color: #ff4b4b;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.title("BMI Calculator")
st.write("Enter your details below to calculate your BMI.")

# Input fields
name = st.text_input("Enter name:", "Joe")
age = st.number_input("Enter age:", min_value=1, max_value=120, value=24)
weight = st.number_input(
    "Enter weight in kilograms:",
    min_value=1.0,
    max_value=500.0,
    value=85.0,
    step=0.5
)
height = st.number_input(
    "Enter height in meters:",
    min_value=0.5,
    max_value=2.8,
    value=1.80,
    step=0.01,
    format="%.2f"
)

# Store people in the session
if "people" not in st.session_state:
    st.session_state.people = []

if st.button("Add Person"):
    if name.strip():
        bmi = weight / (height ** 2)

        if bmi < 18.5:
            category = "Underweight"
        elif bmi < 25:
            category = "Normal weight"
        elif bmi < 30:
            category = "Overweight"
        else:
            category = "Obesity"

        person = {
            "name": name.strip(),
            "age": int(age),
            "weight": weight,
            "height": height,
            "bmi": bmi,
            "category": category
        }

        st.session_state.people.append(person)
        st.success(f"{name} has been added!")
    else:
        st.error("Please enter a name.")

# Results
if st.session_state.people:
    st.subheader("Results")

    for person in st.session_state.people:
        st.write(
            f"**{person['name']}**, Age: {person['age']}, "
            f"Weight: {person['weight']:.1f} kg, "
            f"Height: {person['height']:.2f} m, "
            f"BMI: {person['bmi']:.2f}, "
            f"Category: {person['category']}"
        )

        st.progress(min(person["bmi"] / 40, 1.0))

    if st.button("Clear Results"):
        st.session_state.people = []
        st.rerun()
