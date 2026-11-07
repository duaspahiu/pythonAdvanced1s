import streamlit as st
import pandas as pd

st.title("My First DataFrame")

data = pd.DataFrame({
    "Name": ["John", "Alice", "Bob"],
    "Age": [20, 22, 25]
})

st.write(data)