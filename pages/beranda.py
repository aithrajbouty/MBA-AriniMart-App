import streamlit as st

def app():
    st.title("Beranda")

    st.write(st.session_state['frequent_itemset'])
    st.write(st.session_state['rules'])
    st.write(st.session_state['pola_belanja'])