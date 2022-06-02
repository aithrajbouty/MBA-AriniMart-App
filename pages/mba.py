import streamlit as st
import datetime

def app():
    st.title("Market Basket Analysis")

    # Using "with" notation
    with st.sidebar:
        st.date_input(
            label="When's your birthday",
            value=datetime.date(2019, 7, 6),
            disabled=True)
        # st.write('Your birthday is:', d)

        number = st.number_input('Insert a number')
        st.write('The current number is ', number)

        genre = st.radio(
            "What's your favorite movie genre",
            ('Comedy', 'Drama', 'Documentary'))

        if genre == 'Comedy':
            st.write('You selected comedy.')
        else:
            st.write("You didn't select comedy.")