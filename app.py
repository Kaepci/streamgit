import streamlit as st
import pandas as pd

# Fungsi membaca dataset
@st.cache_data
def baca_csv(nama_file):
    df = pd.read_csv(nama_file)
    return df

# Fungsi untuk mencatat penjualan
def catat_penjualan(df, nama_ikan, jumlah_terjual):
    stok = df.loc[df['Nama_Ikan'] == nama_ikan, 'Jumlah_Stok'].values[0]
    harga = df.loc[df['Nama_Ikan'] == nama_ikan, 'Harga_Per_Kg'].values[0]
    
    if stok >= jumlah_terjual:
        df.loc[df['Nama_Ikan'] == nama_ikan, 'Jumlah_Stok'] -= jumlah_terjual
        pendapatan = jumlah_terjual * harga
        return pendapatan, True
    else:
        return 0, False

# Fungsi untuk menampilkan laporan keuangan
def laporan_keuangan(pendapatan_list):
    return sum(pendapatan_list)

# Fungsi untuk mengunggah dataset baru
def upload_csv():
    st.subheader("Upload Dataset Baru")
    uploaded_file = st.file_uploader("Pilih file CSV", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        df.to_csv('stok_ikan_besar.csv', index=False)
        st.success("Dataset berhasil diunggah dan disimpan!")
        return df
    return None

# Main Streamlit App
def main():
    st.title("Aplikasi Pembukuan Stok Ikan")
    
    # Baca data
    try:
        df = baca_csv('stok_ikan_besar.csv')
    except FileNotFoundError:
        st.warning("Dataset tidak ditemukan. Silakan upload dataset baru!")
        df = upload_csv()

    st.sidebar.header("Menu")
    menu = st.sidebar.selectbox("Pilih Menu", ["Lihat Stok", "Catat Penjualan", "Laporan Keuangan", "Upload Dataset"])
    
    # Fitur Lihat Stok
    if menu == "Lihat Stok":
        st.subheader("Stok Ikan Tersedia")
        if df is not None:
            st.dataframe(df)
        else:
            st.warning("Dataset belum tersedia.")

    # Fitur Catat Penjualan
    elif menu == "Catat Penjualan":
        st.subheader("Catat Penjualan")
        if df is not None:
            nama_ikan = st.selectbox("Pilih Nama Ikan", df['Nama_Ikan'])
            jumlah_terjual = st.number_input("Jumlah yang Terjual (kg)", min_value=0, value=0, step=1)
            
            if st.button("Catat Penjualan"):
                pendapatan, berhasil = catat_penjualan(df, nama_ikan, jumlah_terjual)
                if berhasil:
                    st.success(f"Penjualan berhasil dicatat! Pendapatan: Rp {pendapatan:,}")
                else:
                    st.error("Stok tidak mencukupi!")
        else:
            st.warning("Dataset belum tersedia. Silakan upload dataset terlebih dahulu.")

    # Fitur Laporan Keuangan
    elif menu == "Laporan Keuangan":
        st.subheader("Laporan Keuangan")
        total_pendapatan = laporan_keuangan([0])  # Ganti dengan data pendapatan sebenarnya
        st.write(f"Total Pendapatan: Rp {total_pendapatan:,}")
    
    # Fitur Upload Dataset
    elif menu == "Upload Dataset":
        df = upload_csv()
    
    # Simpan Perubahan Dataset
    if menu != "Upload Dataset" and st.sidebar.button("Simpan Perubahan"):
        if df is not None:
            df.to_csv('stok_ikan_besar.csv', index=False)
            st.sidebar.success("Data berhasil disimpan!")
        else:
            st.sidebar.warning("Tidak ada data untuk disimpan.")

if __name__ == "__main__":
    main()
