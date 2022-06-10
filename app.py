import streamlit as st
# from multiapp import MultiApp
from pages import beranda, info, input, mba
from streamlit_option_menu import option_menu

# Page setting
st.set_page_config(layout="wide")

# session state
if 'df_trx' not in st.session_state:
    st.session_state['df_trx'] = None

if 'eclat_per_item' not in st.session_state:
    st.session_state['eclat_per_item'] = None

if 'basket_per_item' not in st.session_state:
    st.session_state['basket_per_item'] = None

if 'df_kelompok' not in st.session_state:
    st.session_state['df_kelompok'] = None

if 'eclat_per_klmpk' not in st.session_state:
    st.session_state['eclat_per_klmpk'] = None

if 'basket_per_klmpk' not in st.session_state:
    st.session_state['basket_per_klmpk'] = None

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