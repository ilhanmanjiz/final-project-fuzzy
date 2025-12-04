import streamlit as st
import pandas as pd
import numpy as np

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="SPK ISP - SAW & TOPSIS (CRUD)",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INISIALISASI SESSION STATE (DATABASE SEMENTARA) ---
# Ini agar data tidak hilang saat anda klik tombol lain
if 'data_isp' not in st.session_state:
    # Data Default sesuai Excel Anda
    st.session_state['data_isp'] = pd.DataFrame({
        'Alternatif': ['A1 IndiHome', 'A2 Biznet', 'A3 MyRepublic', 'A4 First Media', 'A5 CBN'],
        'C1': [3, 4, 5, 3, 1],       
        'C2': [3, 3, 3, 3, 5],       
        'C3': [1, 5, 3, 1, 5],       
        'C4': [1, 5, 5, 5, 5],       
        'C5': [3, 1, 5, 1, 5]      
    })

if 'bobot' not in st.session_state:
    st.session_state['bobot'] = [0.35, 0.25, 0.20, 0.10, 0.10]

# --- JUDUL APLIKASI ---
st.title("📡 SPK Pemilihan Provider Internet (Fixed Broadband)")
st.markdown("---")

# --- SIDEBAR NAVIGASI ---
with st.sidebar:
    st.header("🗂️ Menu Aplikasi")
    menu = st.radio("Pilih Menu:", ["1. Pengaturan Bobot", "2. Data & CRUD", "3. Hasil Perhitungan"])
    st.info("Aplikasi ini membandingkan metode Fuzzy SAW & TOPSIS.")

# ==========================================
# MENU 1: PENGATURAN BOBOT
# ==========================================
if menu == "1. Pengaturan Bobot":
    st.header("⚙️ Konfigurasi Bobot Kriteria")
    st.write("Sesuaikan tingkat kepentingan kriteria (Total harus 1.0).")
    
    col1, col2 = st.columns(2)
    with col1:
        w1 = st.number_input("C1: Biaya Langganan", 0.0, 1.0, st.session_state['bobot'][0], step=0.05)
        w2 = st.number_input("C2: Kecepatan Download", 0.0, 1.0, st.session_state['bobot'][1], step=0.05)
        w3 = st.number_input("C3: Simetri Upload", 0.0, 1.0, st.session_state['bobot'][2], step=0.05)
    with col2:
        w4 = st.number_input("C4: Batasan FUP", 0.0, 1.0, st.session_state['bobot'][3], step=0.05)
        w5 = st.number_input("C5: Biaya Instalasi", 0.0, 1.0, st.session_state['bobot'][4], step=0.05)

    # Simpan ke session state
    bobot_baru = [w1, w2, w3, w4, w5]
    st.session_state['bobot'] = bobot_baru
    
    total_bobot = sum(bobot_baru)
    st.metric("Total Bobot", f"{total_bobot:.2f}")
    
    if not np.isclose(total_bobot, 1.0):
        st.error("⚠️ Total bobot harus bernilai 1.0")
    else:
        st.success("✅ Bobot valid.")

# ==========================================
# MENU 2: DATA & CRUD (CREATE, READ, UPDATE, DELETE)
# ==========================================
elif menu == "2. Data & CRUD":
    st.header("📝 Manajemen Data Alternatif (CRUD)")
    
    # Tampilkan Data Saat Ini (READ)
    st.subheader("Data Saat Ini")
    st.dataframe(st.session_state['data_isp'], use_container_width=True)
    
    tab_add, tab_edit, tab_del = st.tabs(["➕ Tambah Data", "✏️ Edit Data", "❌ Hapus Data"])
    
    # --- FITUR CREATE (TAMBAH) ---
    with tab_add:
        st.write("Tambah Provider Baru")
        with st.form("form_tambah"):
            new_nama = st.text_input("Nama Alternatif (Contoh: A6 Starlink)")
            c1_new = st.slider("Nilai C1 (Biaya)", 1, 5, 3)
            c2_new = st.slider("Nilai C2 (Speed)", 1, 5, 3)
            c3_new = st.slider("Nilai C3 (Ratio)", 1, 5, 3)
            c4_new = st.slider("Nilai C4 (FUP)", 1, 5, 3)
            c5_new = st.slider("Nilai C5 (Install)", 1, 5, 3)
            
            submit_add = st.form_submit_button("Simpan Data Baru")
            
            if submit_add:
                if new_nama:
                    new_row = pd.DataFrame({
                        'Alternatif': [new_nama],
                        'C1': [c1_new], 'C2': [c2_new], 'C3': [c3_new], 
                        'C4': [c4_new], 'C5': [c5_new]
                    })
                    st.session_state['data_isp'] = pd.concat([st.session_state['data_isp'], new_row], ignore_index=True)
                    st.success(f"Berhasil menambahkan {new_nama}!")
                    st.rerun()
                else:
                    st.warning("Nama alternatif tidak boleh kosong.")

    # --- FITUR UPDATE (EDIT) ---
    with tab_edit:
        st.write("Edit Data yang Ada")
        alternatif_list = st.session_state['data_isp']['Alternatif'].tolist()
        selected_alt = st.selectbox("Pilih Alternatif untuk Diedit", alternatif_list)
        
        if selected_alt:
            # Ambil index data terpilih
            idx = st.session_state['data_isp'][st.session_state['data_isp']['Alternatif'] == selected_alt].index[0]
            current_data = st.session_state['data_isp'].iloc[idx]
            
            with st.form("form_edit"):
                ec1 = st.slider("Edit C1", 1, 5, int(current_data['C1']))
                ec2 = st.slider("Edit C2", 1, 5, int(current_data['C2']))
                ec3 = st.slider("Edit C3", 1, 5, int(current_data['C3']))
                ec4 = st.slider("Edit C4", 1, 5, int(current_data['C4']))
                ec5 = st.slider("Edit C5", 1, 5, int(current_data['C5']))
                
                submit_edit = st.form_submit_button("Update Data")
                
                if submit_edit:
                    st.session_state['data_isp'].at[idx, 'C1'] = ec1
                    st.session_state['data_isp'].at[idx, 'C2'] = ec2
                    st.session_state['data_isp'].at[idx, 'C3'] = ec3
                    st.session_state['data_isp'].at[idx, 'C4'] = ec4
                    st.session_state['data_isp'].at[idx, 'C5'] = ec5
                    st.success(f"Data {selected_alt} berhasil diupdate!")
                    st.rerun()

    # --- FITUR DELETE (HAPUS) ---
    with tab_del:
        st.write("Hapus Data")
        del_options = st.session_state['data_isp']['Alternatif'].tolist()
        to_delete = st.selectbox("Pilih Alternatif untuk Dihapus", del_options)
        
        if st.button("🗑️ Hapus Permanen"):
            st.session_state['data_isp'] = st.session_state['data_isp'][st.session_state['data_isp']['Alternatif'] != to_delete].reset_index(drop=True)
            st.success(f"Berhasil menghapus {to_delete}")
            st.rerun()

# ==========================================
# MENU 3: HASIL PERHITUNGAN
# ==========================================
elif menu == "3. Hasil Perhitungan":
    st.header("📊 Analisis SAW & TOPSIS")
    
    # Cek Validitas Bobot
    bobot_curr = np.array(st.session_state['bobot'])
    if not np.isclose(np.sum(bobot_curr), 1.0):
        st.error("⚠️ Total bobot belum 1.0. Silakan atur di menu 'Pengaturan Bobot'.")
        st.stop()
        
    df = st.session_state['data_isp']
    matrix_x = df.iloc[:, 1:].values.astype(float)
    
    tab_saw, tab_topsis, tab_result = st.tabs(["Metode SAW", "Metode TOPSIS", "Perbandingan"])
    
    # --- METODE SAW ---
    with tab_saw:
        st.subheader("Perhitungan SAW")
        max_values = np.max(matrix_x, axis=0)
        
        # Cegah pembagian nol jika data kosong
        if len(matrix_x) > 0:
            matrix_r_saw = matrix_x / max_values
            
            # Tampilkan R
            df_r = pd.DataFrame(matrix_r_saw, columns=['C1','C2','C3','C4','C5'])
            df_r.insert(0, 'Alternatif', df['Alternatif'])
            st.write("**Matriks Ternormalisasi (R):**")
            st.dataframe(df_r.style.format(subset=['C1','C2','C3','C4','C5'], formatter="{:.2f}"))
            
            # Hitung V
            nilai_v_saw = np.sum(matrix_r_saw * bobot_curr, axis=1)
            
            # Hasil SAW
            df_saw_res = pd.DataFrame({
                'Alternatif': df['Alternatif'],
                'Nilai V': nilai_v_saw
            }).sort_values(by='Nilai V', ascending=False)
            
            st.write("**Hasil Perankingan SAW:**")
            st.dataframe(df_saw_res.style.format({'Nilai V': '{:.3f}'}).highlight_max(color='lightgreen'))
        else:
            st.warning("Belum ada data.")

    # --- METODE TOPSIS ---
    with tab_topsis:
        st.subheader("Perhitungan TOPSIS")
        if len(matrix_x) > 0:
            # 1. Normalisasi Vektor
            pembagi = np.sqrt(np.sum(matrix_x**2, axis=0))
            matrix_r_topsis = matrix_x / pembagi
            
            # 2. Matriks Y
            matrix_y = matrix_r_topsis * bobot_curr
            
            # 3. Solusi Ideal
            a_plus = np.max(matrix_y, axis=0)
            a_min = np.min(matrix_y, axis=0)
            
            # 4. Jarak
            d_plus = np.sqrt(np.sum((matrix_y - a_plus)**2, axis=1))
            d_min = np.sqrt(np.sum((matrix_y - a_min)**2, axis=1))
            
            # 5. Nilai Preferensi
            with np.errstate(divide='ignore', invalid='ignore'):
                nilai_v_topsis = d_min / (d_min + d_plus)
                
            # Hasil TOPSIS
            df_topsis_res = pd.DataFrame({
                'Alternatif': df['Alternatif'],
                'Nilai V': nilai_v_topsis
            }).sort_values(by='Nilai V', ascending=False)
            
            st.write("**Hasil Perankingan TOPSIS:**")
            st.dataframe(df_topsis_res.style.format({'Nilai V': '{:.3f}'}).highlight_max(color='lightblue'))
        else:
            st.warning("Belum ada data.")

    # --- GRAFIK PERBANDINGAN ---
    with tab_result:
        st.subheader("🏆 Komparasi Akhir")
        if len(matrix_x) > 0:
            df_final = pd.DataFrame({
                'Alternatif': df['Alternatif'],
                'Skor SAW': nilai_v_saw,
                'Skor TOPSIS': nilai_v_topsis
            })
            
            st.bar_chart(df_final.set_index('Alternatif'), color=["#FF4B4B", "#1F77B4"])
            
            best_saw = df_saw_res.iloc[0]['Alternatif']
            best_topsis = df_topsis_res.iloc[0]['Alternatif']
            
            st.success(f"Rekomendasi Terbaik (SAW): **{best_saw}**")
            st.info(f"Rekomendasi Terbaik (TOPSIS): **{best_topsis}**")
        else:
            st.warning("Data kosong.")

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("© 2025 SPK Project")