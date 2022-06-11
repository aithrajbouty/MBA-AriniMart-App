from asyncio import base_tasks
import streamlit as st
import pandas as pd
import plotly.express as px
from algorithm import eclat

def app():
    st.title("Info Data")

    with open('./style/style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    global jumlah_trx, jumlah_item, jumlah_klmpk

    if st.session_state['df_trx'] is None or st.session_state['df_klmpk'] is None:
        st.warning("Untuk melihat info data, harap input data transaksi dan/atau data kelompok item terlebih dahulu pada menu Input")

    # cek data transaksi
    if st.session_state['df_trx'] is not None:
        # jumlah untuk info
        jumlah_trx = len(st.session_state['df_trx']['PENJUALAN_ID'].unique())
        jumlah_item = len(st.session_state.df_trx['INVENTARIS_NAMABARANG'].unique())

        # data untuk bar chart
        df_total_item = pd.DataFrame(st.session_state['basket_per_item'].sum())
        df_total_item.index.name = "item"
        df_total_item.rename(columns={0: 'Total'}, inplace=True)
        items_terbanyak = df_total_item.sort_values(by="Total", ascending=False).head(10)

        # bar chart
        fig_items = px.bar(
            items_terbanyak,
            x=items_terbanyak.index,
            y="Total",
            title="<b> 10 Item Terbanyak Dibeli",
            color_discrete_sequence=["#529AEF"] * len(items_terbanyak),
            template="plotly_white"
        )        
    else:
        jumlah_trx = "-"
        jumlah_item = "-"
        fig_items = None
        # st.warning("Harap input data transaksi penjualan pada menu Input")

    # cek data kelompok
    if st.session_state['df_kelompok'] is not None:
        # jumlah untuk info
        jumlah_klmpk = len(st.session_state.df_kelompok['KELOMPOK_ITEM'].unique())
        
        # data untuk bar chart
        df_total_klmpk = pd.DataFrame(st.session_state['basket_per_klmpk'].sum())
        df_total_klmpk.index.name = "kelompok"
        df_total_klmpk.rename(columns={0: 'Total'}, inplace=True)
        klmpk_terbanyak = df_total_klmpk.sort_values(by="Total", ascending=False).head(10)

        # bar chart
        fig_klmpk = px.bar(
            klmpk_terbanyak,
            x=klmpk_terbanyak.index,
            y="Total",
            title="<b> 10 Kelompok Item Terbanyak Dibeli",
            color_discrete_sequence=["#529AEF"] * len(items_terbanyak),
            template="plotly_white"
        )  
    else:
        jumlah_klmpk = "-"
        fig_klmpk = None
        # st.warning("Harap input data kelompok item pada menu Input")

    # Row A
    a1, a2, a3 = st.columns(3)
    a1.metric("Jumlah Transaksi", jumlah_trx)
    a2.metric("Jumlah Item", jumlah_item)
    a3.metric("Jumlah Kelompok Item", jumlah_klmpk)

    b1, b2 = st.columns(2)
    with b1:
        if fig_items is not None:
            st.plotly_chart(fig_items)
        # else:
        #     st.write("10 Item Terbanyak Dibeli")
    
    with b2:
        if fig_klmpk is not None:
            st.plotly_chart(fig_klmpk)
        # else:
        #     st.write("10 Kelompok Item Terbanyak Dibeli")

    # # Row B
    # if fig_items is not None:
    #     st.plotly_chart(fig_items)
    # # else:
    # #     st.write("10 Item Terbanyak Dibeli")

    # # Row C
    # if fig_klmpk is not None:
    #     st.plotly_chart(fig_klmpk)
    # # else:
    # #     st.write("10 Item Terbanyak Dibeli")