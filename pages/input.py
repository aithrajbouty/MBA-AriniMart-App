import streamlit as st
import pandas as pd
import inspect
from st_aggrid import AgGrid
from algorithm import eclat

def app():
    st.title("Input")

    global df_trx, kelompok_item, df_kelompok, trx_per_item, eclat_per_item, basket_per_item, trx_per_klmpk, eclat_per_klmpk, basket_per_klmpk

    # Upload file transaksi
    st.markdown('### Data Transaksi Penjualan')
    file_transaksi = st.file_uploader(
        label="Unggah file data transaksi di sini",
        type=['xlsx'],
        accept_multiple_files=False
    )
    st.write(file_transaksi)

    def buat_dfTrx():
        with st.spinner('Memroses Data...'):
            df_trx = pd.read_excel(file_transaksi)
            trx_headers = ['PENJUALAN_ID', 'PENJUALAN_TANGGAL', 'PENJUALAN_WAKTU', 'PENJUALAN_NILAI', 'DETIL_KODEBARANG', 'DETIL_SATUAN_JUMLAH', 'DETIL_SATUAN_HARGA', 'DETIL_TOTAL', 'INVENTARIS_NAMABARANG']
            cek_df_trx = [i for i in df_trx.columns if i not in trx_headers]

            # cek kalau data benar sesuai dengan yang diminta
            if cek_df_trx == []:
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

            else:
                st.error("Data yang anda masukkan salah! Data transaksi penjualan harus memiliki kolom seperti berikut: " + str(trx_headers)[1:-1] + ". Harap masukkan data yang sesuai")
                st.session_state['df_trx'] = None
                st.session_state['eclat_per_item'] = None
                st.session_state['basket_per_item'] = None

    if file_transaksi is not None:
        if st.session_state['df_trx'] is None:
            buat_dfTrx()
        elif st.session_state['df_trx'] is not None:
            st.session_state['df_kelompok'] = None
            st.session_state['eclat_per_klmpk'] = None
            st.session_state['basket_per_klmpk'] = None

            buat_dfTrx()
    
    try:
        if st.session_state['df_trx'] is not None:
            AgGrid(st.session_state['df_trx'], theme='streamlit')
        else:
            st.write("")
    except Exception as e:
        print(e)
        st.write("")
    
  
    # Upload file kelompok item 
    st.markdown('### Data Kelompok Item')
    if st.session_state['df_trx'] is None:
        disabled = True
        st.warning("Data kelompok tidak dapat diinput apabila data transaksi belum diinput")
    else:
        disabled = False

    file_kelompok = st.file_uploader(
        label="Unggah file data kelompok item di sini",
        type=['xlsx'],
        disabled= disabled,
        accept_multiple_files=False
    )

    if file_kelompok is not None:
        with st.spinner('Memroses Data...'):
            kelompok_item = pd.read_excel(file_kelompok)
            st.session_state['kelompok_item'] = kelompok_item
            klmpk_headers = ['items', 'kelompok']
            cek_df_klmpk = [i for i in kelompok_item.columns if i not in klmpk_headers]

            # cek kalau data benar
            if cek_df_klmpk == []:
                # buat df dengan kelompok item
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

            else:
                st.error("Data yang anda masukkan salah! Data kelompok item harus memiliki kolom seperti berikut: " + str(klmpk_headers)[1:-1] + ". Harap masukkan data yang sesuai")
                st.session_state['df_kelompok'] = None
                st.session_state['eclat_per_klmpk'] = None
                st.session_state['basket_per_klmpk'] = None
        
    try:
        if st.session_state['df_kelompok'] is not None:
            AgGrid(st.session_state['kelompok_item'], theme='streamlit')
            st.write('Data transaksi berdasarkan kelompok item:')
            AgGrid(st.session_state['df_kelompok'], theme='streamlit')
        else:
            st.write("")
    except Exception as e:
        print(e)
        st.write("")