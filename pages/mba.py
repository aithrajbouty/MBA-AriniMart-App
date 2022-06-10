import streamlit as st
import datetime
from algorithm import eclat
from pages import input

def bg_colour_col (col):
    colour = '#ffff00'
    return ['background-color: %s' % colour 
                if col.name=='support' or i==4   # color column `Total` or row `4`
                else ''
             for i,x in col.iteritems()]

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

    if 'maxCombination' not in st.session_state:
        st.session_state['maxCombination'] = None

    if 'frequent_itemset' not in st.session_state:
        st.session_state['frequent_itemset'] = None

    if 'rules' not in st.session_state:
        st.session_state['rules'] = None

    if 'pola_belanja' not in st.session_state:
        st.session_state['pola_belanja'] = None




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

        maxCombination = st.slider(
            label='Kombinasi Maksimum', 
            value=2,
            min_value=1,
            max_value=3,
            key=int,
            disabled=disabled
        )

        def handle_click(new_tipe, new_bentuk_support, new_support, new_confidence, newMaxCombination):
            st.session_state['frequent_itemset'] = None
            st.session_state['rules'] = None
            st.session_state['pola_belanja'] = None
            st.session_state['tipe_analisis'] = new_tipe
            st.session_state['bentuk_support'] = new_bentuk_support
            st.session_state['support'] = new_support
            st.session_state['confidence'] = new_confidence
            st.session_state['maxCombination'] = newMaxCombination

        lakukan_analisis = st.button(
            label="Lakukan Analisis", 
            on_click=handle_click, 
            args=[tipe_analisis, bentuk_support, support, confidence, maxCombination],
            disabled=disabled)

    if st.session_state['tipe_analisis'] is None or st.session_state['bentuk_support'] is None or st.session_state['support'] is None or st.session_state['confidence'] is None or st.session_state['maxCombination'] is None:
        st.write("")
    else:
        st.write('tipe_analisis: ', st.session_state['tipe_analisis'])
        st.write('bentuk_support: ', st.session_state['bentuk_support'])
        st.write('support: ', st.session_state['support'])
        st.write('confidence: ', st.session_state['confidence'])
        st.write('maxCombination: ', st.session_state['maxCombination'])

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

        # cari frequent itemset
        st.markdown("## Frequent Itemset")
        if st.session_state['frequent_itemset'] is None:
            eclat_indexes, eclat_supports = eclat.cari_freq_itemset(
                data=data,
                basket=basket,
                minTrx=minTrx,
                minValue=st.session_state['support'],
                maxComb=st.session_state['maxCombination']
            )
            frequent_itemset = eclat.reshape_freq_itemset(eclat_support=eclat_supports)
            st.session_state['frequent_itemset'] = frequent_itemset

            freq_itemset = frequent_itemset.copy()
            freq_itemset["itemsets"] = freq_itemset["itemsets"].apply(lambda x: ', '.join(list(x))).astype("unicode")
            freq_itemset.style.apply(bg_colour_col)
            st.write(freq_itemset)
        else:
            freq_itemset = st.session_state['frequent_itemset'].copy()
            freq_itemset["itemsets"] = freq_itemset["itemsets"].apply(lambda x: ', '.join(list(x))).astype("unicode")
            st.write(freq_itemset)

        # cari association rules
        st.markdown("## Association Rules")
        if st.session_state['rules'] is None:
            rules = eclat.cari_assoc_rules(
                freq_itemset=st.session_state['frequent_itemset'],
                minconf=st.session_state['confidence']
            )
            st.session_state['rules'] = rules
            st.write(st.session_state['rules'])
        else:
            st.write(st.session_state['rules'])

        # buat pola belanja konsumen
        st.markdown("## Pola Belanja Konsumen")
        if st.session_state['pola_belanja'] is None:
            pola_belanja_konsumen = eclat.buat_pola_belanja(st.session_state['rules'])
            st.session_state['pola_belanja'] = pola_belanja_konsumen
            st.write(pola_belanja_konsumen)
        else:
            st.write(st.session_state['pola_belanja'])



    
    
































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