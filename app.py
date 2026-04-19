import streamlit as st
import time
import pandas as pd
from gauss_jordan import gauss_jordan_steps
from determinant import (
    determinant_obe_steps, determinant_sarrus_steps, 
    determinant_cofactor_steps, can_use_sarrus
)
from inverse import inverse_adjoint_steps, inverse_obe_steps

#--PAGE CONFIG--
st.set_page_config(
    page_title="Kalkulator Matriks", 
    layout="centered"
)

#--LOAD CONFIG--
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title("🧮 Kalkulator Matriks")

tab1, tab2, tab3 = st.tabs(["📐 Gauss-Jordan", "🔢 Determinan", "🔄 Invers"])

#====================TAB 1: GAUSS JORDAN====================
with tab1:
    st.markdown("""
    <div class='info-box'>
        <strong>📐 Eliminasi Gauss-Jordan</strong><br>
        Menyelesaikan Sistem Persamaan Linear (SPL) dengan reduksi matriks.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        n = st.slider("Jumlah Kolom", 2, 6, 3, key="gj_cols")
    with col2:
        m = st.slider("Jumlah Baris", 2, 6, 3, key="gj_rows")
    
    st.markdown("### Input Matriks: ")
    
    matrix = []
    for i in range(n):
        cols = st.columns(m)
        row = []
        for j in range(m):
            label = f"a{i+1}{j+1}" if j < m-1 else f"b{i+1}"
            val = cols[j].number_input(label, key=f"gj_{i}_{j}", format="%f")
            row.append(val)
        matrix.append(row)
    
    if st.button("Hitung Gauss-Jordan", use_container_width=True):
        with st.spinner("Menghitung..."):
            time.sleep(0.2)
            hasil, langkah, solusi = gauss_jordan_steps(matrix)
            
            if hasil is None:
                st.error(f"❌ {solusi}")
            else:
                st.success("✅ Selesai!")
                
                st.markdown("### Jenis Solusi")
                if solusi == "Solusi unik":
                    st.info("Solusi tunggal")
                elif solusi == "Solusi tak hingga":
                    st.warning("Solusi tak hingga")
                else:
                    st.error("Tidak ada solusi")
                
                st.markdown("### Hasil Akhir")
                st.dataframe(pd.DataFrame(hasil.tolist()), use_container_width=True)
                
                st.markdown("### Langkah-langkah")
                for i, step in enumerate(langkah):
                    with st.expander(f"Langkah {i+1}"):
                        st.write(step["desc"])
                        st.dataframe(pd.DataFrame(step["matrix"].tolist()), use_container_width=True)

#====================TAB 2: DETERMINAN====================
with tab2:
    st.markdown("""
    <div class='info-box'>
        <strong>🔢 Kalkulator Determinan</strong><br>
        Metode: OBE, Sarrus (2x2 & 3x3), dan Ekspansi Kofaktor.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        det_method = st.selectbox(
            "Pilih Metode",
            ["Operasi Baris Elementer (OBE)", "Ekspansi Kofaktor", "Sarrus"]
        )
    
    with col2:
        if det_method == "Sarrus":
            det_n = st.selectbox("Ordo Matriks", [2, 3], key="det_size")
        else:
            det_n = st.slider("Ordo Matriks (n x n)", 2, 6, 3, key="det_size")
    
    if det_method == "Sarrus" and det_n not in [2, 3]:
        st.warning("⚠️ Metode Sarrus hanya untuk matriks 2x2 atau 3x3")
    
    st.markdown(f"### Input Matriks {det_n} x {det_n}")
    
    det_matrix = []
    for i in range(det_n):
        cols = st.columns(det_n)
        row = []
        for j in range(det_n):
            val = cols[j].number_input(f"M{i+1}{j+1}", key=f"det_{i}_{j}", value=0.0, format="%f")
            row.append(val)
        det_matrix.append(row)
    
    if st.button("Hitung Determinan", use_container_width=True):
        with st.spinner("Menghitung..."):
            time.sleep(0.2)
            
            if det_method == "Sarrus":
                if det_n == 2 or det_n == 3:
                    result, steps = determinant_sarrus_steps(det_matrix)
                    if isinstance(result, float) and result == int(result):
                        result = int(result)
                    st.success(f"✅ Determinan = **{result}**")
                    
                    st.markdown("### Langkah-langkah")
                    for step in steps:
                        with st.expander(step['title']):
                            st.write(step["desc"])
                            if step.get("matrix"):
                                st.write(step["matrix"])
                else:
                    st.error("❌ Metode Sarrus hanya untuk matriks 2x2 atau 3x3!")
            
            elif det_method == "Operasi Baris Elementer (OBE)":
                result, steps = determinant_obe_steps(det_matrix)
                if result is None:
                    st.error("❌ Gagal menghitung determinan")
                else:
                    if isinstance(result, float) and result == int(result):
                        result = int(result)
                    st.success(f"✅ Determinan = **{result}**")
                    
                    st.markdown("### Langkah-langkah")
                    for step in steps:
                        with st.expander(step['title']):
                            st.write(step["desc"])
                            if step.get("matrix"):
                                st.dataframe(pd.DataFrame(step["matrix"]), use_container_width=True)
            
            else:  #--KOFAKTOR--
                result, steps = determinant_cofactor_steps(det_matrix)
                if isinstance(result, float) and result == int(result):
                    result = int(result)
                st.success(f"✅ Determinan = **{result}**")
                
                st.markdown("### Langkah-langkah")
                for step in steps:
                    with st.expander(step['title']):
                        st.write(step["desc"])
                        if step.get("matrix"):
                            st.write(step["matrix"])

#====================TAB 3: INVERS====================
with tab3:
    st.markdown("""
    <div class='info-box'>
        <strong>🔄 Kalkulator Invers Matriks</strong><br>
        Metode: Adjoin dan OBE. Matriks harus determinan ≠ 0.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        inv_method = st.selectbox("Pilih Metode", ["Adjoin", "Operasi Baris Elementer (OBE)"])
    
    with col2:
        inv_n = st.slider("Ordo Matriks (n x n)", 2, 6, 3, key="inv_size")
    
    st.markdown(f"### Input Matriks {inv_n} x {inv_n}")
    
    inv_matrix = []
    for i in range(inv_n):
        cols = st.columns(inv_n)
        row = []
        for j in range(inv_n):
            val = cols[j].number_input(f"N{i+1}{j+1}", key=f"inv_{i}_{j}", value=0.0, format="%f")
            row.append(val)
        inv_matrix.append(row)
    
    if st.button("Hitung Invers", use_container_width=True):
        with st.spinner("Menghitung invers..."):
            time.sleep(0.2)
            
            if inv_method == "Adjoin":
                result, steps, message = inverse_adjoint_steps(inv_matrix)
                
                if result is None:
                    st.error(f"❌ {message}")
                else:
                    st.success("✅ Invers berhasil!")
                    st.markdown("### Hasil Invers")
                    result_clean = []
                    for row in result:
                        clean_row = []
                        for val in row:
                            if isinstance(val, float) and val == int(val):
                                clean_row.append(int(val))
                            else:
                                clean_row.append(round(val, 6))
                        result_clean.append(clean_row)
                    st.dataframe(pd.DataFrame(result_clean), use_container_width=True)
                    
                    st.markdown("### Langkah-langkah")
                    for step in steps:
                        with st.expander(step['title']):
                            st.write(step["desc"])
                            if step.get("matrix"):
                                if isinstance(step["matrix"], list):
                                    matrix_clean = []
                                    for row in step["matrix"]:
                                        clean_row = []
                                        for val in row:
                                            if isinstance(val, float) and val == int(val):
                                                clean_row.append(int(val))
                                            else:
                                                clean_row.append(round(val, 6) if isinstance(val, float) else val)
                                        matrix_clean.append(clean_row)
                                    st.dataframe(pd.DataFrame(matrix_clean), use_container_width=True)
            
            else:  #--OBE--
                result, steps, message = inverse_obe_steps(inv_matrix)
                
                if result is None:
                    st.error(f"❌ {message}")
                else:
                    st.success("✅ Invers berhasil!")
                    st.markdown("### Hasil Invers")
                    result_clean = []
                    for row in result:
                        clean_row = []
                        for val in row:
                            if isinstance(val, float) and val == int(val):
                                clean_row.append(int(val))
                            else:
                                clean_row.append(round(val, 6))
                        result_clean.append(clean_row)
                    st.dataframe(pd.DataFrame(result_clean), use_container_width=True)
                    
                    st.markdown("### Langkah-langkah")
                    for step in steps:
                        with st.expander(step['title']):
                            st.write(step["desc"])
                            if step.get("matrix"):
                                matrix_clean = []
                                for row in step["matrix"]:
                                    clean_row = []
                                    for val in row:
                                        if isinstance(val, float) and val == int(val):
                                            clean_row.append(int(val))
                                        else:
                                            clean_row.append(round(val, 6) if isinstance(val, float) else val)
                                    matrix_clean.append(clean_row)
                                st.dataframe(pd.DataFrame(matrix_clean), use_container_width=True)
