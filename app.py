from flask import Flask, render_template, request, redirect, url_for, make_response, send_file
import mysql.connector
from fpdf import FPDF
import os

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'rapor_anisa'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

def generate_id_nilai():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id_nilai
        FROM tb_nilai_anisa
        WHERE id_nilai LIKE 'NLI%'
        ORDER BY CAST(SUBSTRING(id_nilai, 4) AS UNSIGNED) DESC
        LIMIT 1
    """)
    row = cursor.fetchone()

    if row:
        nomor = int(row['id_nilai'][3:]) + 1
    else:
        nomor = 1

    cursor.close()
    conn.close()

    return f"NLI{nomor:03d}"

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'RAPOR SISWA', 0, 1, 'C')
        self.ln(5)

@app.route('/')
def index():
    return redirect(url_for('daftar_nilai'))

@app.route('/nilai')
def daftar_nilai():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Ambil parameter filter dari URL
    kelas = request.args.get('kelas', '')
    semester = request.args.get('semester', '')

    # Query dasar
    query = """
        SELECT
            n.id_nilai,
            s.nis,
            s.nama_siswa,
            k.nama_kelas,
            m.nama_mapel,
            n.nilai_tugas,
            n.nilai_uts,
            n.nilai_uas,
            n.deskripsi,
            ROUND((n.nilai_tugas + n.nilai_uts + n.nilai_uas) / 3, 2) AS nilai_akhir,
            n.semester,
            n.tahun_ajaran
        FROM tb_nilai_anisa n
        JOIN tb_siswa_anisa s ON n.nis = s.nis
        JOIN tb_kelas_anisa k ON s.id_kelas = k.id_kelas
        JOIN tb_mapel_anisa m ON n.id_mapel = m.id_mapel
        WHERE 1=1
    """
    
    params = []
    
    # Tambahkan filter berdasarkan parameter
    if kelas:
        query += " AND k.nama_kelas = %s"
        params.append(kelas)
    
    if semester:
        query += " AND n.semester = %s"
        params.append(semester)
    
    query += " ORDER BY s.nama_siswa, m.nama_mapel"

    cursor.execute(query, params)
    data = cursor.fetchall()

    # Ambil daftar kelas untuk dropdown filter
    cursor.execute("SELECT DISTINCT nama_kelas FROM tb_kelas_anisa ORDER BY nama_kelas")
    kelas_list = cursor.fetchall()

    # Ambil daftar semester unik untuk dropdown
    cursor.execute("SELECT DISTINCT semester FROM tb_nilai_anisa ORDER BY semester")
    semester_list = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('hasil_koneksi.html', 
                         siswa=data, 
                         kelas_list=kelas_list,
                         semester_list=semester_list,
                         filter_kelas=kelas,
                         filter_semester=semester)

@app.route('/edit_nilai/<id_nilai>', methods=['GET', 'POST'])
def edit_nilai(id_nilai):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        id_mapel = request.form['id_mapel']
        nilai_tugas = request.form['nilai_tugas']
        nilai_uts = request.form['nilai_uts']
        nilai_uas = request.form['nilai_uas']
        semester = request.form['semester']
        tahun_ajaran = request.form['tahun_ajaran']
        deskripsi = request.form['deskripsi']

        query = """
        UPDATE tb_nilai_anisa SET
            id_mapel=%s,
            nilai_tugas=%s,
            nilai_uts=%s,
            nilai_uas=%s,
            semester=%s,
            tahun_ajaran=%s,
            deskripsi=%s
        WHERE id_nilai=%s
        """

        cursor.execute(query, (
            id_mapel,
            nilai_tugas,
            nilai_uts,
            nilai_uas,
            semester,
            tahun_ajaran,
            deskripsi,
            id_nilai
        ))

        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('daftar_nilai'))

    cursor.execute("""
        SELECT n.*, m.nama_mapel
        FROM tb_nilai_anisa n
        JOIN tb_mapel_anisa m ON n.id_mapel = m.id_mapel
        WHERE n.id_nilai=%s
    """, (id_nilai,))
    nilai = cursor.fetchone()

    cursor.execute("SELECT id_mapel, nama_mapel FROM tb_mapel_anisa")
    mapel = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('edit_nilai.html', nilai=nilai, mapel=mapel)

@app.route('/delete_nilai/<id_nilai>')
def delete_nilai(id_nilai):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tb_nilai_anisa WHERE id_nilai=%s", (id_nilai,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('daftar_nilai'))

@app.route('/tambah_nilai', methods=['GET', 'POST'])
def tambah_nilai():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        id_nilai = generate_id_nilai()
        nis = request.form['nis']
        id_mapel = request.form['id_mapel']
        nilai_tugas = request.form['nilai_tugas']
        nilai_uts = request.form['nilai_uts']
        nilai_uas = request.form['nilai_uas']
        semester = request.form['semester']
        tahun_ajaran = request.form['tahun_ajaran']
        deskripsi = request.form['deskripsi']

        query = """
            INSERT INTO tb_nilai_anisa
            (id_nilai, nis, id_mapel, nilai_tugas, nilai_uts, nilai_uas,
             semester, tahun_ajaran, deskripsi)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        cursor.execute(query, (
            id_nilai, nis, id_mapel,
            nilai_tugas, nilai_uts, nilai_uas,
            semester, tahun_ajaran, deskripsi
        ))
        conn.commit()

        cursor.close()
        conn.close()
        return redirect(url_for('daftar_nilai'))

    cursor.execute("SELECT nis, nama_siswa FROM tb_siswa_anisa")
    siswa = cursor.fetchall()

    cursor.execute("SELECT id_mapel, nama_mapel FROM tb_mapel_anisa")
    mapel = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('tambah_nilai.html', siswa=siswa, mapel=mapel)

# ======================= CETAK HTML =======================
@app.route('/cetak/<nis>')
def cetak_rapor(nis):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT s.nis, s.nama_siswa, k.nama_kelas
        FROM tb_siswa_anisa s
        JOIN tb_kelas_anisa k ON s.id_kelas = k.id_kelas
        WHERE s.nis = %s
    """, (nis,))
    siswa = cursor.fetchone()

    cursor.execute("""
         SELECT n.nis,
                m.nama_mapel,
                n.nilai_tugas,
                n.nilai_uts,
                n.nilai_uas,
                ROUND((n.nilai_tugas + n.nilai_uts + n.nilai_uas)/3, 2) AS nilai_akhir,
                n.deskripsi,
                n.semester,
                n.tahun_ajaran
        FROM tb_nilai_anisa n
        JOIN tb_mapel_anisa m ON n.id_mapel = m.id_mapel
        WHERE n.nis = %s
    """, (nis,))
    nilai = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('cetak_rapor.html', siswa=siswa, nilai=nilai)

# ======================= CETAK PDF (langsung download) =======================
@app.route('/cetak_pdf/<nis>')
def cetak_pdf_siswa(nis):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Ambil data siswa
    cursor.execute("""
        SELECT s.nis, s.nama_siswa, k.nama_kelas
        FROM tb_siswa_anisa s
        JOIN tb_kelas_anisa k ON s.id_kelas = k.id_kelas
        WHERE s.nis = %s
    """, (nis,))
    siswa = cursor.fetchone()

    if not siswa:
        cursor.close()
        conn.close()
        return "Data siswa tidak ditemukan"

    # Ambil data nilai
    cursor.execute("""
        SELECT m.nama_mapel,
               n.nilai_tugas,
               n.nilai_uts,
               n.nilai_uas,
               ROUND((n.nilai_tugas + n.nilai_uts + n.nilai_uas)/3, 2) AS nilai_akhir,
               n.deskripsi,
               n.semester,
               n.tahun_ajaran
        FROM tb_nilai_anisa n
        JOIN tb_mapel_anisa m ON n.id_mapel = m.id_mapel
        WHERE n.nis = %s
    """, (nis,))
    nilai = cursor.fetchall()

    cursor.close()
    conn.close()

    # Buat PDF
    pdf = PDF()
    pdf.add_page()
    
    # Set font (gunakan Arial default atau tambahkan font custom jika perlu)
    pdf.set_font('Arial', '', 12)
    
    # Header
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'RAPOR SISWA', 0, 1, 'C')
    pdf.ln(10)
    
    # Data Siswa
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 8, f"NIS          : {siswa['nis']}", ln=True)
    pdf.cell(0, 8, f"Nama Siswa   : {siswa['nama_siswa']}", ln=True)
    pdf.cell(0, 8, f"Kelas        : {siswa['nama_kelas']}", ln=True)
    
    if nilai:
        pdf.cell(0, 8, f"Semester     : {nilai[0]['semester']}", ln=True)
        pdf.cell(0, 8, f"Tahun Ajaran : {nilai[0]['tahun_ajaran']}", ln=True)
    
    pdf.ln(10)
    
    # Tabel Nilai
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(40, 10, "Mata Pelajaran", 1, 0, 'C')
    pdf.cell(25, 10, "Tugas", 1, 0, 'C')
    pdf.cell(25, 10, "UTS", 1, 0, 'C')
    pdf.cell(25, 10, "UAS", 1, 0, 'C')
    pdf.cell(25, 10, "Nilai Akhir", 1, 0, 'C')
    pdf.cell(50, 10, "Deskripsi", 1, 1, 'C')
    
    pdf.set_font('Arial', '', 11)
    for d in nilai:
        pdf.cell(40, 8, d['nama_mapel'], 1)
        pdf.cell(25, 8, str(d['nilai_tugas']), 1, 0, 'C')
        pdf.cell(25, 8, str(d['nilai_uts']), 1, 0, 'C')
        pdf.cell(25, 8, str(d['nilai_uas']), 1, 0, 'C')
        pdf.cell(25, 8, str(d['nilai_akhir']), 1, 0, 'C')
        pdf.cell(50, 8, d['deskripsi'], 1, 1)
    
    # Tambahkan catatan di bawah
    pdf.ln(10)
    pdf.set_font('Arial', 'I', 10)
    pdf.cell(0, 8, "Catatan: Nilai akhir dihitung dari rata-rata (Tugas + UTS + UAS) / 3", 0, 1)
    
    # Simpan ke file sementara
    file_name = f"Rapor_{siswa['nis']}_{siswa['nama_siswa'].replace(' ', '_')}.pdf"
    file_path = f"temp_{file_name}"
    
    pdf.output(file_path)
    
    # Kirim file sebagai attachment
    response = send_file(
        file_path,
        as_attachment=True,
        download_name=file_name,
        mimetype='application/pdf'
    )
    
    # Hapus file temporary setelah dikirim (opsional)
    @response.call_on_close
    def cleanup():
        try:
            os.remove(file_path)
        except:
            pass
    
    return response

if __name__ == '__main__':
    app.run(debug=True)