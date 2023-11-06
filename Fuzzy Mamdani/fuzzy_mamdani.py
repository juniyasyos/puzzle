import numpy as np
import pandas as pd

from flask import Flask, render_template

app = Flask(__name__, template_folder="hah")

class PengendaliFuzzyMamdani:
    def __init__(self, variabel_input, variabel_output):
        self.variabel_input = variabel_input
        self.variabel_output = variabel_output
        self.aturan = []

    def tambahkan_aturan(self, antaseden, konsekuens):
        aturan = {'antaseden': antaseden, 'konsekuens': konsekuens}
        self.aturan.append(aturan)

    def fuzzifikasi_input(self, nilai_input):
        # Fuzzifikasi nilai input menggunakan fungsi keanggotaan
        nilai_fuzzy_input = {}
        for nama_var, nilai in nilai_input.items():
            var = self.variabel_input[nama_var]
            nilai_fuzzy = {}
            for nama_term, (a, b) in var.items():
                nilai_fuzzy[nama_term] = self.fungsi_keanggotaan(nilai, a, b)
            nilai_fuzzy_input[nama_var] = nilai_fuzzy
        return nilai_fuzzy_input

    def terapkan_aturan(self, nilai_fuzzy_input):
        # Terapkan aturan-aturan fuzzy untuk menentukan himpunan fuzzy output
        himpunan_fuzzy_output = {}
        for aturan in self.aturan:
            antaseden, konsekuens = aturan['antaseden'], aturan['konsekuens']
            kekuatan_aturan = min([nilai_fuzzy_input[var][term] for var, term in antaseden])
            for var, term in konsekuens:
                if (var, term) not in himpunan_fuzzy_output:
                    himpunan_fuzzy_output[(var, term)] = []
                himpunan_fuzzy_output[(var, term)].append(kekuatan_aturan)
        return himpunan_fuzzy_output

    def defuzzifikasi_output(self, himpunan_fuzzy_output):
        # Defuzzifikasi himpunan fuzzy output untuk mendapatkan nilai tegas
        nilai_tegas_output = {}
        for (var, term), kekuatan in himpunan_fuzzy_output.items():
            kekuatan_tergabung = np.max(kekuatan)  # Anda dapat menggunakan metode penggabungan yang berbeda
            nilai_tegas = self.fungsi_keanggotaan_tergabung(var, term, kekuatan_tergabung)
            nilai_tegas_output[(var, term)] = nilai_tegas
        return nilai_tegas_output

    def fungsi_keanggotaan(self, x, a, b):
        return max(0, min((x - a) / (b - a), (b - x) / (b - a)))

    def fungsi_keanggotaan_tergabung(self, var, term, kekuatan_tergabung):
        a, b = self.variabel_output[var][term]
        daerah = np.linspace(a, b, 1000)
        num = sum(min(self.fungsi_keanggotaan(x, a, b), kekuatan_tergabung) * x for x in daerah)
        den = sum(min(self.fungsi_keanggotaan(x, a, b), kekuatan_tergabung) for x in daerah)
        return num / (den + 1e-10)  # Tambahkan epsilon ke penyebut untuk menghindari pembagian oleh nol

@app.route('/')
def halaman_utama():
    # Inisialisasi variabel-variabel input dan output
    variabel_input = {
        'Kain' : {
            'SEDIKIT': [410, 677],
            'SEDANG': [543.5, 810.5],
            'BANYAK': [677, 944]
        },
        'Malam' : {
            'SEDIKIT': [51.25, 84.6],
            'SEDANG': [67.9, 101.3],
            'BANYAK': [84.6, 118]
        },
        'Pewarna' : {
            'SEDIKIT': [102.5, 169.3],
            'SEDANG': [135.9, 202.6],
            'BANYAK': [169.3, 236]
        },
        'BiayaProduksi' : {
            'SEDIKIT': [5350500, 10988350],
            'SEDANG': [8169425, 13807275],
            'BANYAK': [10988350, 16626200]
        },
        'Permintaan' : {
            'SEDIKIT': [196, 341],
            'SEDANG': [268, 413],
            'BANYAK': [341, 485]
        },
        'Stok' : {
            'SEDIKIT': [22, 49],
            'SEDANG': [35, 62],
            'BANYAK': [49, 75]
        }}


    variabel_output = {
        'JumlahProduksi' : {
            'SEDIKIT': [205, 339],
            'SEDANG': [272, 405],
            'BANYAK': [339, 472]
            }}

    # Inisialisasi pengendali fuzzy Mamdani
    pengendali_fuzzy = PengendaliFuzzyMamdani(variabel_input, variabel_output)
    
    # Aturan-aturan fuzzy (10 aturan)
    pengendali_fuzzy.tambahkan_aturan([
        ('Kain', 'SEDIKIT'),
        ('Malam', 'SEDIKIT'),
        ('Pewarna', 'SEDIKIT'),
        ('BiayaProduksi', 'SEDIKIT'),
        ('Permintaan', 'SEDIKIT'),
        ('Stok', 'SEDIKIT')
    ], [('JumlahProduksi', 'SEDIKIT')])

    pengendali_fuzzy.tambahkan_aturan([
        ('Kain', 'SEDANG'),
        ('Malam', 'SEDANG'),
        ('Pewarna', 'SEDANG'),
        ('BiayaProduksi', 'SEDIKIT'),
        ('Permintaan', 'SEDANG'),
        ('Stok', 'SEDANG')
    ], [('JumlahProduksi', 'BANYAK')])

    pengendali_fuzzy.tambahkan_aturan([
        ('Kain', 'SEDIKIT'),
        ('Malam', 'SEDANG'),
        ('Pewarna', 'SEDANG'),
        ('BiayaProduksi', 'SEDIKIT'),
        ('Permintaan', 'SEDIKIT'),
        ('Stok', 'SEDIKIT')
    ], [('JumlahProduksi', 'SEDIKIT')])

    pengendali_fuzzy.tambahkan_aturan([
        ('Kain', 'SEDANG'),
        ('Malam', 'SEDANG'),
        ('Pewarna', 'SEDANG'),
        ('BiayaProduksi', 'SEDIKIT'),
        ('Permintaan', 'SEDIKIT'),
        ('Stok', 'SEDIKIT')
    ], [('JumlahProduksi', 'BANYAK')])

    pengendali_fuzzy.tambahkan_aturan([
        ('Kain', 'SEDIKIT'),
        ('Malam', 'SEDIKIT'),
        ('Pewarna', 'SEDIKIT'),
        ('BiayaProduksi', 'SEDANG'),
        ('Permintaan', 'SEDIKIT'),
        ('Stok', 'SEDIKIT')
    ], [('JumlahProduksi', 'SEDIKIT')])

    pengendali_fuzzy.tambahkan_aturan([
        ('Kain', 'SEDANG'),
        ('Malam', 'SEDANG'),
        ('Pewarna', 'SEDANG'),
        ('BiayaProduksi', 'SEDANG'),
        ('Permintaan', 'SEDIKIT'),
        ('Stok', 'SEDIKIT')
    ], [('JumlahProduksi', 'BANYAK')])

    pengendali_fuzzy.tambahkan_aturan([
        ('Kain', 'SEDIKIT'),
        ('Malam', 'SEDIKIT'),
        ('Pewarna', 'SEDIKIT'),
        ('BiayaProduksi', 'SEDIKIT'),
        ('Permintaan', 'SEDANG'),
        ('Stok', 'SEDANG')
    ], [('JumlahProduksi', 'BANYAK')])

    pengendali_fuzzy.tambahkan_aturan([
        ('Kain', 'SEDANG'),
        ('Malam', 'SEDANG'),
        ('Pewarna', 'SEDANG'),
        ('BiayaProduksi', 'SEDANG'),
        ('Permintaan', 'SEDANG'),
        ('Stok', 'SEDANG')
    ], [('JumlahProduksi', 'BANYAK')])

    pengendali_fuzzy.tambahkan_aturan([
        ('Kain', 'SEDANG'),
        ('Malam', 'SEDANG'),
        ('Pewarna', 'SEDANG'),
        ('BiayaProduksi', 'SEDANG'),
        ('Permintaan', 'SEDIKIT'),
        ('Stok', 'SEDIKIT')
    ], [('JumlahProduksi', 'SEDANG')])

    pengendali_fuzzy.tambahkan_aturan([
        ('Kain', 'SEDANG'),
        ('Malam', 'SEDANG'),
        ('Pewarna', 'SEDANG'),
        ('BiayaProduksi', 'SEDANG'),
        ('Permintaan', 'SEDIKIT'),
        ('Stok', 'SEDIKIT')
    ], [('JumlahProduksi', 'SEDANG')])

    pengendali_fuzzy.tambahkan_aturan([
        ('Kain', 'SEDANG'),
        ('Malam', 'SEDANG'),
        ('Pewarna', 'SEDANG'),
        ('BiayaProduksi', 'SEDANG'),
        ('Permintaan', 'SEDIKIT'),
        ('Stok', 'SEDIKIT')
    ], [('JumlahProduksi', 'SEDANG')])

    pengendali_fuzzy.tambahkan_aturan([
        ('Kain', 'SEDANG'),
        ('Malam', 'SEDANG'),
        ('Pewarna', 'SEDANG'),
        ('BiayaProduksi', 'SEDANG'),
        ('Permintaan', 'SEDIKIT'),
        ('Stok', 'SEDIKIT')
    ], [('JumlahProduksi', 'SEDANG')])

    pengendali_fuzzy.tambahkan_aturan([
        ('Kain', 'SEDANG'),
        ('Malam', 'SEDANG'),
        ('Pewarna', 'SEDANG'),
        ('BiayaProduksi', 'SEDANG'),
        ('Permintaan', 'SEDIKIT'),
        ('Stok', 'SEDIKIT')
    ], [('JumlahProduksi', 'SEDANG')])

    # Contoh 10 nilai input
    nilai_input_1 = {
        'Kain': 550,
        'Malam': 85,
        'Pewarna': 170,
        'BiayaProduksi': 11000000,
        'Permintaan': 280,
        'Stok': 50
    }

    nilai_input_2 = {
        'Kain': 480,
        'Malam': 75,
        'Pewarna': 160,
        'BiayaProduksi': 10500000,
        'Permintaan': 260,
        'Stok': 45
    }

    nilai_input_3 = {
        'Kain': 700,
        'Malam': 95,
        'Pewarna': 190,
        'BiayaProduksi': 12500000,
        'Permintaan': 320,
        'Stok': 58
    }

    nilai_input_4 = {
        'Kain': 620,
        'Malam': 88,
        'Pewarna': 175,
        'BiayaProduksi': 11200000,
        'Permintaan': 290,
        'Stok': 53
    }

    nilai_input_5 = {
        'Kain': 530,
        'Malam': 80,
        'Pewarna': 165,
        'BiayaProduksi': 10800000,
        'Permintaan': 270,
        'Stok': 47
    }

    nilai_input_6 = {
        'Kain': 590,
        'Malam': 92,
        'Pewarna': 185,
        'BiayaProduksi': 11800000,
        'Permintaan': 310,
        'Stok': 56
    }

    nilai_input_7 = {
        'Kain': 510,
        'Malam': 78,
        'Pewarna': 162,
        'BiayaProduksi': 10600000,
        'Permintaan': 265,
        'Stok': 49
    }

    nilai_input_8 = {
        'Kain': 650,
        'Malam': 89,
        'Pewarna': 180,
        'BiayaProduksi': 11400000,
        'Permintaan': 285,
        'Stok': 52
    }

    nilai_input_9 = {
        'Kain': 570,
        'Malam': 86,
        'Pewarna': 168,
        'BiayaProduksi': 10900000,
        'Permintaan': 275,
        'Stok': 48
    }

    nilai_input_10 = {
        'Kain': 630,
        'Malam': 93,
        'Pewarna': 187,
        'BiayaProduksi': 11900000,
        'Permintaan': 315,
        'Stok': 54
    }

    nilai_input = [nilai_input_1, nilai_input_2, nilai_input_3, nilai_input_4, nilai_input_5, nilai_input_6, nilai_input_7, nilai_input_8, nilai_input_9, nilai_input_10]

    # Fuzzifikasi input
    nilai_fuzzy_input = [pengendali_fuzzy.fuzzifikasi_input(i) for i in nilai_input]

    # Terapkan aturan fuzzy
    himpunan_fuzzy_output = [pengendali_fuzzy.terapkan_aturan(i) for i in nilai_fuzzy_input]

    # Defuzzifikasi output
    nilai_tegas_output = [pengendali_fuzzy.defuzzifikasi_output(i) for i in himpunan_fuzzy_output]

    # Menampilkan hasil dalam bentuk tabel
    hasil_df = [pd.DataFrame.from_dict(i, orient='index', columns=['Nilai Tegas Output']) for i in nilai_tegas_output]

    # Menyiapkan data untuk ditampilkan di halaman HTML
    variable_input = variabel_input
    variable_output = variabel_output
    aturan_diterapkan = pengendali_fuzzy.aturan
    nilai_inputan = nilai_input

    return render_template('hasil_defuzzifikasi.html',
                           variable_input=variable_input,
                           variable_output=variable_output,
                           aturan_diterapkan=aturan_diterapkan,
                           nilai_inputan=nilai_inputan,
                           hasil_df=hasil_df)


if __name__ == '__main__':
    app.run(debug=True)
