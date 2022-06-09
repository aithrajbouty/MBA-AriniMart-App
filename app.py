import streamlit as st
# from multiapp import MultiApp
from pages import beranda, info, input, mba
from streamlit_option_menu import option_menu

# Page setting
st.set_page_config(layout="wide")

# Menu
selected = option_menu(
    menu_title=None,
    options=["Beranda", "Input", "Info Data", "Analisis Data"],
    default_index=0,
    orientation="horizontal"
)

if selected == "Beranda":
    beranda.app()
if selected == "Input":
    input.app()
if selected == "Info Data":
    info.app()
if selected == "Analisis Data":
    mba.app()