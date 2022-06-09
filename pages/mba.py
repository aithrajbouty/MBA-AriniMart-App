import streamlit as st
import datetime
from algorithm import eclat
from pages import input

def app():
    st.title("Market Basket Analysis")

    # set sessions
    if 'tipe_analisis' not in st.session_state:
        st.session_state['tipe_analisis'] = None

    if 'bentuk_support' not in st.session_state:
        st.session_state['bentuk_support'] = None

    if 'support' not in st.session_state:
        st.session_state['support'] = None

    if 'confidence' not in st.session_state:
        st.session_state['confidence'] = None

    if 'frequent_itemset' not in st.session_state:
        st.session_state['frequent_itemset'] = None

    if 'rules' not in st.session_state:
        st.session_state['rules'] = None




    if st.session_state['df_trx'] is None and st.session_state['df_kelompok'] is None:
        st.write("Harap input data transaksi penjualan pada menu Input sebelum melakukan analisis. Untuk melakukan analisis berdasarkan item, harap input data kelompok item pada menu Input")
        list_analisis = ['Item', 'Kelompok Item']
        disabled = True
    elif st.session_state['df_kelompok'] is None:
        st.write("Perhatian: Anda hanya dapat melakukan analisis berdasarkan item karena data kelompok item belum diinput")
        list_analisis = ['Item']
        disabled = False
    else:
        list_analisis = ['Item', 'Kelompok Item']
        disabled = False

    # widgets
    with st.sidebar:
        tipe_analisis = st.radio(
            label="Lakukan analisis berdasarkan",
            options=(list_analisis),
            disabled=disabled
        )

        bentuk_support = st.radio(
            label="Untuk menginput nilai support minimum dapat dilakukan dengan cara menginput:",
            options=('Nilai Support (Contoh: 0,01)', 'Jumlah Transaksi (Contoh: 500)'),
            disabled=disabled
        )

        support = st.number_input(
            label='Nilai Support Minimum', 
            value=0.01,
            disabled=disabled
        )

        confidence = st.number_input(
            label='Nilai Confidence Minimum', 
            value=0.3,
            disabled=disabled
        )

        def handle_click(new_tipe, new_bentuk_support, new_support, new_confidence):
            st.session_state['tipe_analisis'] = new_tipe
            st.session_state['bentuk_support'] = new_bentuk_support
            st.session_state['support'] = new_support
            st.session_state['confidence'] = new_confidence

        lakukan_analisis = st.button(
            label="Lakukan Analisis", 
            on_click=handle_click, 
            args=[tipe_analisis, bentuk_support, support, confidence],
            disabled=disabled)

    if st.session_state['tipe_analisis'] is None or st.session_state['bentuk_support'] is None or st.session_state['support'] is None or st.session_state['confidence'] is None:
        st.write("")
    else:
        st.write('tipe_analisis: ', st.session_state['tipe_analisis'])
        st.write('bentuk_support: ', st.session_state['bentuk_support'])
        st.write('support: ', st.session_state['support'])
        st.write('confidence: ', st.session_state['confidence'])

        if(st.session_state.tipe_analisis == "Item"):
            data = st.session_state['eclat_per_item']
            basket = st.session_state['eclat_per_klmpk']
        elif(st.session_state.tipe_analisis == "Kelompok Item"):
            data = st.session_state['eclat_per_klmpk']
            basket = st.session_state['basket_per_klmpk']

        if(bentuk_support == 'Nilai Support (Contoh: 0,01)'):
            minTrx = False
        else:
            minTrx = True   

        eclat_indexes, eclat_supports = eclat.cari_freq_itemset(
            data=data,
            basket=basket,
            minTrx=minTrx,
            minValue=st.session_state['support']
        )

        # cari frequent itemset
        st.session_state['frequent_itemset'] = eclat.reshape_freq_itemset(eclat_support=eclat_supports)
        st.markdown("## Frequent Itemset")
        st.write(st.session_state['frequent_itemset'])

        # cari association rules
        st.session_state['rules'] = eclat.cari_assoc_rules(
            frequent_itemsets=st.session_state['frequent_itemset'],
            minconf=st.session_state['confidence']
        )
        st.markdown("## Association Rules")
        st.write(st.session_state['rules'])



    
    
































    # # if 'birthday' not in st.session_state or 'genre' not in st.session_state:
    #     st.session_state['birthday'] = datetime.date(2019, 7, 6);
    #     st.session_state['genre'] = 'Comedy'

    # # Using "with" notation
    # with st.sidebar:
    #     birthday = st.date_input(
    #         label="When's your birthday",
    #         value=datetime.date(2019, 7, 6),
    #         # disabled=True
    #         )

    #     genre = st.radio(
    #         "What's your favorite movie genre",
    #         ('Comedy', 'Drama', 'Documentary'))
        
    #     def handle_click(new_birthday, new_genre):
    #         st.session_state.birthday = new_birthday
    #         st.session_state.genre = new_genre

    #     st.button("Compute", on_click=handle_click, args=[birthday, genre])

    # st.write(st.session_state['birthday'])
    # st.write(st.session_state['genre'])