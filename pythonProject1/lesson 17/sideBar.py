import streamlit as st

st.sidebar.header("sidebar")

st.sidebar.header("this is a sidebar")

st.sidebar.selectbox("chose an option",["oprion 1","oprion 2","oprion"])
st.sidebar.radio("go to",["Home","settings"])