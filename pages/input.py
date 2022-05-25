import streamlit as st
import pandas as pd
from algorithm import eclat

def app():
    st.title("Input")

    global df_trx, kelompok_item, df_kelompok, trx_per_item, eclat_per_item, basket_per_item, trx_per_klmpk, eclat_per_klmpk, basket_per_klmpk

    # Upload file transaksi
    file_transaksi = st.file_uploader(label="Unggah file data transaksi di sini",
                                        type=['xlsx'])
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
    try:
        st.write(df_trx)
    except Exception as e:
        print(e)
        st.write("")
  
    # Upload file kelompok item 
    file_kelompok = st.file_uploader(label="Unggah file data kelompok item di sini",
                                        type=['xlsx'])
    if file_kelompok is not None:
        kelompok_item = pd.read_excel(file_kelompok)

        # buat df dengan kelompok item
        if df_trx is not None:
            df_kelompok = df_trx.copy()
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
        
    try:
        st.write(kelompok_item)
        st.write(df_kelompok)
    except Exception as e:
        print(e)
        st.write("")
    
def get_df_trx():
    try:
        df_trx
        return df_trx
    except Exception as e:
        print(e)
        return None

def get_basket_item():
    try:
        basket_per_item
        return basket_per_item
    except Exception as e:
        print(e)
        return None
    
def get_df_klmpk():
    try:
        df_kelompok
        return df_kelompok
    except Exception as e:
        print(e)
        return None

def get_basket_klmpk():
    try:
        basket_per_klmpk
        return basket_per_klmpk
    except Exception as e:
        print(e)
        return None
