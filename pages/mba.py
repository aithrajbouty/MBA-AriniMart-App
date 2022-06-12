import streamlit as st
import pandas as pd
import datetime
from st_aggrid import AgGrid
from algorithm import eclat
from pages import input

def app():
    st.header("Market Basket Analysis")

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
        st.warning("Harap input data transaksi penjualan pada menu Input sebelum melakukan analisis. Untuk melakukan analisis berdasarkan item, harap input data kelompok item pada menu Input")
        list_analisis = ['Item', 'Kelompok Item']
        disabled = True
    elif st.session_state['df_kelompok'] is None:
        st.info("Perhatian: Anda hanya dapat melakukan analisis berdasarkan item karena data kelompok item belum diinput")
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
        if(st.session_state.tipe_analisis == "Item"):
            data = st.session_state['eclat_per_item']
            basket = st.session_state['basket_per_item']
        elif(st.session_state.tipe_analisis == "Kelompok Item"):
            data = st.session_state['eclat_per_klmpk']
            basket = st.session_state['basket_per_klmpk']

        if(st.session_state['bentuk_support'] == 'Nilai Support (Contoh: 0,01)'):
            minTrx = False
            minSupport = (f"{round((st.session_state['support']) * 100,2)}{'%'}")
        else:
            minTrx = True   
            totalTransactions = len(basket.index)
            minSupport = (f"{round(st.session_state['support']/totalTransactions * 100,2)}{'%'}")
        
        minConf = (f"{round((st.session_state['confidence']) * 100,2)}{'%'}")

        parameters = {
            'Tipe analisis':[st.session_state['tipe_analisis']],
            'Nilai support minimum':[minSupport],
            'Nilai confidence minimum': [minConf],
            'Kombinasi Maksimum': [st.session_state['maxCombination']]
        }
        parameters_df = pd.DataFrame(parameters)
        styler = parameters_df.style.hide_index()
        st.write(styler.to_html(), unsafe_allow_html=True)

        # cari frequent itemset
        st.markdown("### Frequent Itemset")
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
            # freq_itemset.style.apply(bg_colour_col)
            AgGrid(freq_itemset, theme='streamlit')
        else:
            freq_itemset = st.session_state['frequent_itemset'].copy()
            freq_itemset["itemsets"] = freq_itemset["itemsets"].apply(lambda x: ', '.join(list(x))).astype("unicode")
            AgGrid(freq_itemset, theme='streamlit')

        # cari association rules
        st.markdown("### Association Rules")
        if st.session_state['rules'] is None:
            rules = eclat.cari_assoc_rules(
                freq_itemset=st.session_state['frequent_itemset'],
                minconf=st.session_state['confidence']
            )
            st.session_state['rules'] = rules

            st.markdown(''' 
            - _Support_: presentase item terhadap total item yang berada pada dataset transaksi
            - _Confidence_: ukuran yang menunjukkan hubungan antar dua atau lebih item secara kondisional, misal menghitung kemungkinan item _consequent_ dibeli oleh pelanggan jika pelanggan membeli item _antecedent_
            - _Lift_: mengukur seberapa sering _antecedent_ dan _consequent_ pada terjadi secara bersama-sama dan apakah mereka independen. Nilai _lift_ = 1 artinya _antecedent_ dan _consequent_ bersifat independen
            - _Leverage_: digunakan untuk menghitung perbedaan antara frekuensi _antecedent_ dan _consequent_ yang mucnul bersamaan. Nilai _leverage_ = 0 artinya _antecedent_ dan _consequent_ bersifat independen
            - _Conviction_: menghitung tingkat implikasi aturan dan juga menilai independensi antara A dan B. Nilai _conviction_ = 0 artinya _antecedent_ dan _consequent_ bersifat
            ''')
            AgGrid(st.session_state['rules'], theme='streamlit')
        else:
            AgGrid(st.session_state['rules'], theme='streamlit')

        # buat pola belanja konsumen
        st.markdown("### Pola Belanja Konsumen")
        if st.session_state['pola_belanja'] is None:
            pola_belanja_konsumen = eclat.buat_pola_belanja(st.session_state['rules'])
            st.session_state['pola_belanja'] = pola_belanja_konsumen
            AgGrid(pola_belanja_konsumen, theme='streamlit', fit_columns_on_grid_load=True)
        else:
            AgGrid(st.session_state['pola_belanja'], theme='streamlit', fit_columns_on_grid_load=True)