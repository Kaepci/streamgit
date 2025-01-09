import streamlit as st
import pandas as pd

# Fungsi membaca dataset
@st.cache_data
def baca_csv(nama_file):
    return pd.read_csv(nama_file)

# Fungsi untuk mencatat penjualan
def catat_penjualan(df, nama_ikan, jumlah_terjual):
    stok = df.loc[df['Nama_Ikan'] == nama_ikan, 'Jumlah_Stok'].values[0]
    harga = df.loc[df['Nama_Ikan'] == nama_ikan, 'Harga_Per_Kg'].values[0]
    
    if stok >= jumlah_terjual:
        # Update stok di dataset
        df.loc[df['Nama_Ikan'] == nama_ikan, 'Jumlah_Stok'] -= jumlah_terjual
        pendapatan = jumlah_terjual * harga
        return pendapatan, True
    else:
        return 0, False

# Fungsi untuk menyimpan dataset
def simpan_csv(df, nama_file):
    df.to_csv(nama_file, index=False)

# Fungsi untuk menghitung laporan keuangan
def laporan_keuangan(pendapatan_list):
    return sum(pendapatan_list)

# Main Streamlit App
def main():
    st.title("Aplikasi Pembukuan Stok Ikan")
    
    # File dataset
    file_dataset = 'stok_ikan_besar.csv'
    
    # Baca data
    try:
        df = baca_csv(file_dataset)
    except FileNotFoundError:
        st.warning("Dataset tidak ditemukan. Silakan upload dataset baru!")
        return

    # Sidebar menu
    st.sidebar.header("Menu")
    menu = st.sidebar.selectbox("Pilih Menu", ["Lihat Stok", "Catat Penjualan", "Laporan Keuangan", "Upload Dataset"])
    
    # Fitur Lihat Stok
    if menu == "Lihat Stok":
        st.subheader("Stok Ikan Tersedia")
        st.dataframe(df)

    # Fitur Catat Penjualan
    elif menu == "Catat Penjualan":
        st.subheader("Catat Penjualan")
        nama_ikan = st.selectbox("Pilih Nama Ikan", df['Nama_Ikan'])
        jumlah_terjual = st.number_input("Jumlah yang Terjual (kg)", min_value=0, value=0, step=1)
        
        if st.button("Catat Penjualan"):
            pendapatan, berhasil = catat_penjualan(df, nama_ikan, jumlah_terjual)
            if berhasil:
                simpan_csv(df, file_dataset)  # Simpan perubahan ke file
                st.success(f"Penjualan berhasil dicatat! Pendapatan: Rp {pendapatan:,}")
                st.dataframe(df)  # Tampilkan dataset terbaru
            else:
                st.error("Stok tidak mencukupi untuk transaksi ini.")

    # Fitur Laporan Keuangan
    elif menu == "Laporan Keuangan":
        st.subheader("Laporan Keuangan")
        # Total pendapatan simulasi (seharusnya diambil dari catatan penjualan jika ada)
        total_pendapatan = laporan_keuangan([0])  # Ganti dengan pendapatan sebenarnya
        st.write(f"Total Pendapatan: Rp {total_pendapatan:,}")

    # Fitur Upload Dataset
    elif menu == "Upload Dataset":
        st.subheader("Upload Dataset Baru")
        uploaded_file = st.file_uploader("Pilih file CSV", type="csv")
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            df.to_csv(file_dataset, index=False)
            st.success("Dataset berhasil diunggah dan disimpan!")
            st.dataframe(df)

if __name__ == "__main__":
    main()
