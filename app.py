import streamlit as st
from pages import beranda, info, input, mba
from streamlit_option_menu import option_menu

# Page setting
st.set_page_config(layout="wide")

with open('./style/style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# session state
if 'df_trx' not in st.session_state:
    st.session_state['df_trx'] = None

if 'eclat_per_item' not in st.session_state:
    st.session_state['eclat_per_item'] = None

if 'basket_per_item' not in st.session_state:
    st.session_state['basket_per_item'] = None

if 'kelompok_item' not in st.session_state:
    st.session_state['kelompok_item'] = None

if 'df_kelompok' not in st.session_state:
    st.session_state['df_kelompok'] = None

if 'eclat_per_klmpk' not in st.session_state:
    st.session_state['eclat_per_klmpk'] = None

if 'basket_per_klmpk' not in st.session_state:
    st.session_state['basket_per_klmpk'] = None

st.title('Aplikasi MBA AriniMart')

# Menu
selected = option_menu(
    menu_title=None,
    options=["Beranda", "Input", "Info Data", "Analisis Data"],
    default_index=0,
    orientation="horizontal",
    icons=['house-door', 'cloud-arrow-up', 'bar-chart-line', 'graph-up']
)

if selected == "Beranda":
    beranda.app()
if selected == "Input":
    input.app()
if selected == "Info Data":
    info.app()
if selected == "Analisis Data":
    mba.app()