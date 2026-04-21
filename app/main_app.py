import streamlit as st

st.title("JobSeek AI")
st.subheader("AI-powered Job Search Platform")

st.write("Welcome to JobSeek AI 🚀")

query = st.text_input("Search job")

if st.button("Search"):
    st.write(f"Searching for: {query}")