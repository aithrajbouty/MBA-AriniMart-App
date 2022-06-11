import streamlit as st
import pandas as pd
from algorithm import eclat

def app():
    st.title("Input")

    global df_trx, kelompok_item, df_kelompok, trx_per_item, eclat_per_item, basket_per_item, trx_per_klmpk, eclat_per_klmpk, basket_per_klmpk

    # Upload file transaksi
    file_transaksi = st.file_uploader(
        label="Unggah file data transaksi di sini",
        type=['xlsx']
    )

    if file_transaksi is not None:
        df_trx = pd.read_excel(file_transaksi)

        # masukkan data ke eclat
        trx_per_item = eclat.reshape_dataset(
            dataset=df_trx, 
            kolom="INVENTARIS_NAMABARANG"
        )
        eclat_per_item, basket_per_item = eclat.eclat_basket(
            data_trx=trx_per_item
        )
        
        st.session_state['df_trx'] = df_trx
        st.session_state['eclat_per_item'] = eclat_per_item
        st.session_state['basket_per_item'] = basket_per_item
    try:
        if st.session_state['df_trx'] is not None:
            st.write(st.session_state['df_trx'])
        else:
            st.write("")
    except Exception as e:
        print(e)
        st.write("")
  
    # Upload file kelompok item 
    if st.session_state['df_trx'] is None:
        disabled = True
        st.warning("Data kelompok tidak dapat diinput apabila data transaksi belum diinput")
    else:
        disabled = False

    file_kelompok = st.file_uploader(
        label="Unggah file data kelompok item di sini",
        type=['xlsx'],
        disabled= disabled
    )

    if file_kelompok is not None:
        kelompok_item = pd.read_excel(file_kelompok)

        # buat df dengan kelompok item
        if st.session_state['df_trx'] is not None:
            df_kelompok = st.session_state['df_trx'].copy()
            df_kelompok['INVENTARIS_NAMABARANG'] = df_kelompok['INVENTARIS_NAMABARANG'].map(kelompok_item.set_index('items')['kelompok'])
            df_kelompok.rename(columns={'INVENTARIS_NAMABARANG':'KELOMPOK_ITEM'}, inplace=True)
            df_kelompok = df_kelompok.drop_duplicates(subset = ['PENJUALAN_ID', 'KELOMPOK_ITEM'], keep = 'last')
            
        # masukkan data ke eclat
        trx_per_klmpk = eclat.reshape_dataset(
            dataset=df_kelompok,
            kolom='KELOMPOK_ITEM'
        )
        eclat_per_klmpk, basket_per_klmpk = eclat.eclat_basket(
            data_trx=trx_per_klmpk,
        )

        st.session_state['df_kelompok'] = df_kelompok
        st.session_state['eclat_per_klmpk'] = eclat_per_klmpk
        st.session_state['basket_per_klmpk'] = basket_per_klmpk
        
    try:
        if st.session_state['df_kelompok'] is not None:
            st.write(st.session_state['df_kelompok'])
        else:
            st.write("")
    except Exception as e:
        print(e)
        st.write("")