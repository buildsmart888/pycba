# This file is temporarily disabled to avoid conflicts
import streamlit as st

st.set_page_config(
    page_title="Disabled",
    page_icon="⚠️",
    layout="wide"
)

st.title("⚠️ File Disabled")
st.warning("This page has been disabled to resolve conflicts.")

if st.button("🏠 Go Home"):
    st.switch_page("home.py")
