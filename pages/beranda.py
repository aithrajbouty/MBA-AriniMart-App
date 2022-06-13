import streamlit as st

def app():
    st.header('Apakah Fungsi dari Aplikasi Ini?')
    st.markdown(''' 
    Aplikasi ini berfungsi untuk melakukan analisis pada data transaksi penjualan AriniMart dengan menggunakan metode  _Market Basket Analysis_. Pengguna dapat melakukan dua macam analisis, yaitu analisis berdasarkan item dan analisis berdasarkan kelompok item.
    ''')

    st.markdown('## Apa itu _Market Basket Analysis_?')
    st.markdown(''' 
    _Market Basket Analysis_ (MBA) atau yang dapat diartikan sebagai analisis keranjang belanja, yang merupakan salah satu metode dalam _data mining_. Dengan menggunakan MBA, kita dapat mengetahui perilaku kebiasaan konsumen dalam pembelian barang, sehingga dapat diketahui asosiasi barang-barang yang seringkali dibeli secara bersamaan atau yang disebut juga sebagai _frequent itemset_. Pencarian asosiasi dilakukan dengan mengolah data pembelian barang dari setiap transaksi penjualan, kemudian dicari hubungan antar barang-barang tersebut.
    ''')

    st.markdown('## Kegunaan _Market Basket Analysis_')
    st.markdown(''' 
    Toko AriniMart dapat menggunakan _market basket analysis_ untuk menciptakan strategi bisnis yang dapat digunakan untuk bersaing dengan bisnis lain. Dengan memanfaatkan informasi yang dihasilkan oleh analisis, yaitu barang-barang yang seringkali dibeli secara bersamaan, bisnis dapat menyusun strategi seperti menyediakan stok barang yang diminati konsumen ataupun melakukan penataan tata letak barang pada rak.
    ''')

    st.header('Fungsi Menu')
    st.markdown(''' 
    1. **Menu beranda**: membaca Informasi mengenai aplikasi
    2. **Menu Input Data**:
        - Pengguna dapat menginput data transaksi penjualan AriniMart dan data kelompok item (opsional).
        - Data yang diinputkan adalah data dengan tipe excel (.xlsx)
        - Data transaksi penjualan yang diinputkan **DIHARUSKAN** memiliki bentuk seperti berikut:
            | PENJUALAN_ID | PENJUALAN_TANGGAL | PENJUALAN_WAKTU | DETIL_KODEBARANG | DETIL_SATUAN_JUMLAH | DETIL_SATUAN_HARGA | DETIL_TOTAL | INVENTARIS_NAMABARANG |
            | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
            | 432692663 | 20/03/2021 | 13:27 | 45000 | 8997016379379 | 1 | 13000 | 13000 | Miranda HC MC-18 |
            | 102570928 | 20/03/2021 | 14:48 | 413600 | 8997017642229 | 1 | 21700 | 21700 | Evangeline ruby 100ml |
            | 102570928 | 20/03/2021 | 14:48 | 413600 | 8997025913120 | 1 | 5700 | 5700 | Hatari cocopuff cklt 170g |
        
        - Apabila pengguna ingin melakukan analisis berdasarkan kelompok item, pengguna **WAJIB** menginputkan data kelompok item yang berbentuk seperti berikut:
            | items | kelompok |
            | ----------- | ----------- |
            | Indomie kari ayam 70g | mi instan |
            | Sun Pisang 120 g | makanan bayi |
            | Lays rumput laut 40 g | camilan |
    3. **Menu Info Data**:
        - Pengguna dapat melihat informasi mengenai data yang sudah diinput
        - Informasi data yang disajikan berupa: jumlah transaksi, jumlah item, jumlah kelompok item, dan grafik 10 item dan kelompok item terbanyak dibeli
    4. **Menu Analisis Data**:
        - Untuk melakukan market basket analysis pada data yang sudah diinputkan
        - Pengguna **WAJIB** mengisi persyaratan analisis atau parameter yang berada pada sidebar di bagian kanan, yaitu:
            - Pilih untuk melakukan analisis berdasarkan item atau berdasarkan kelompok item
            - Jenis nilai support yang akan diinput. Pengguna dapat menginput nilai support secara langsung, yaitu dalam bentuk decimal/persenan: kalau 1% masukkan 0,01. Atau pengguna dapat memasukkan jumlah transaksi minimum item/kelompok item muncul pada data transaksi -> nilai support akan dihitung oleh aplikasi
            - Nilai _support_ minimum. Jika menggunakan nilai support langsung, masukkan dalam bentuk desimal (kalau 1% -> masukkan 0,01). Kalau pakai jumlah transaksi, langsung masukkan jumlah transaksinya (contoh 500)
            - Nilai _confidence minimum_. Digunakan untuk mencari _association rules_
            - Kombinasi maksimal yang akan dihasilkan
        - Hasil analisis adalah tiga macam tabel, yaitu:
            - **_Frequent itemset_**: Pola kombinasi objek atau item yang frekuensinya banyak ditemukan pada dataset atau disebut juga sebagai _frequent itemset_. Item dalam itemset dapat berjumlah satu atau lebih.
            - **_Association rules_**: Aturan asosiasi atau kaidah asosiasi yang menunjukkan hubungan antar dua atau lebih item.
            - **Pola belanja konsumen**: Pola belanja konsumen dan persenan keyakinannya yang didapatkan dari hasil _association rules_.
    ''')