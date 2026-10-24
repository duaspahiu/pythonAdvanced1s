import streamlit as st

from pythonProject1.perseritje.loops import names

with st.form ("my_form", clear_on_submit=True):
    name = st.text_input("name")

    age = st.slider("Age",min_value=0,max_value=100)

    email = st.text_input("Email")

    biography = st.text_input("short bio")

    terms = st.checkbox("I agree to the terms and conditions")

    sumbmit_button = st.form_submit_button(label='submit')

if sumbmit_button:
    st.write("Name of the person is:",name)
    st.write("Age of the person is:", age)
    st.write("email of the person is:" ,email)
    st.write("bio of the person is:", biography)

    if terms:
        st.write("you agreed to the terms and conditions")
    else:
        st.write("you did not agree with terms and conditions")
