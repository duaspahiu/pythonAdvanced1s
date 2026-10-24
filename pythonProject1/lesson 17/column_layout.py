import streamlit as at

col1,col2,col3,col3,col4,col5 = st.columns(5, gap="small", vertical_alignment="center")

with col1:
    st.header("kjo eshte kolona e pare")

    st.write("kjo eshte kolona e pare")
with col2:
    st.header("kolona e dyte")

    st.write("kjo eshte kolona e pare")
with col3:
    st.header("kolona e dyte")

    st.write("kjo eshte kolona e pare")
with col3:
    st.header("kolona e kater")

    st.write("kjo weshte kolona e pare")
with col5:
    st.header("kolona e pest")

    st.write("kjo eshte kolona e pare")