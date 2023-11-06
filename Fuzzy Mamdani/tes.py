import numpy as np
import pandas as pd
from icecream import ic

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
            # ic(nilai_fuzzy_input)
            # ic(nilai_fuzzy_input[nama_var])
        return nilai_fuzzy_input

    def terapkan_aturan(self, nilai_fuzzy_input):
        # Terapkan aturan-aturan fuzzy untuk menentukan himpunan fuzzy output
        himpunan_fuzzy_output = {}
        for aturan in self.aturan:
            ic(aturan)
            antaseden, konsekuens = aturan['antaseden'], aturan['konsekuens']
            kekuatan_aturan = min([nilai_fuzzy_input[var][term] for var, term in antaseden])
            ic(kekuatan_aturan)
            for var, term in konsekuens:
                if (var, term) not in himpunan_fuzzy_output:
                    himpunan_fuzzy_output[(var, term)] = []
                himpunan_fuzzy_output[(var, term)].append(kekuatan_aturan)
                ic(himpunan_fuzzy_output)
        return himpunan_fuzzy_output

    def defuzzifikasi_output(self, himpunan_fuzzy_output):
        # Defuzzifikasi himpunan fuzzy output untuk mendapatkan nilai tegas
        nilai_tegas_output = {}
        for (var, term), kekuatan in himpunan_fuzzy_output.items():
            kekuatan_tergabung = np.max(kekuatan)  # Anda dapat menggunakan metode penggabungan yang berbeda
            nilai_tegas = self.fungsi_keanggotaan_tergabung(var, term, kekuatan_tergabung)
            nilai_tegas_output[(var, term)] = nilai_tegas
        ic(nilai_tegas_output)
        return nilai_tegas_output

    def fungsi_keanggotaan(self, x, a, b):
        # ic(max(0, min((x - a) / (b - a), (b - x) / (b - a))))
        # ic(min((x - a) / (b - a), (b - x) / (b - a)))
        return max(0, min((x - a) / (b - a), (b - x) / (b - a)))

    def fungsi_keanggotaan_tergabung(self, var, term, kekuatan_tergabung):
        a, b = self.variabel_output[var][term]
        daerah = np.linspace(a, b, 1000)
        num = sum(min(self.fungsi_keanggotaan(x, a, b), kekuatan_tergabung) * x for x in daerah)
        den = sum(min(self.fungsi_keanggotaan(x, a, b), kekuatan_tergabung) for x in daerah)
        return num / (den + 1e-10)  # Tambahkan epsilon ke penyebut untuk menghindari pembagian oleh nol


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

    # Masukkan nilai input
    nilai_kain = 600
    nilai_malam = 90
    nilai_pewarna = 180
    nilai_biaya_produksi = 12000000
    nilai_permintaan = 300
    nilai_stok = 55

    # Anda dapat menggunakan nilai-nilai ini dalam fungsi fuzzifikasi_input pada pengendali logika fuzzy Anda
    nilai_input = {
        'Kain': nilai_kain,
        'Malam': nilai_malam,
        'Pewarna': nilai_pewarna,
        'BiayaProduksi': nilai_biaya_produksi,
        'Permintaan': nilai_permintaan,
        'Stok': nilai_stok
    }

    # Fuzzifikasi input
    nilai_fuzzy_input = pengendali_fuzzy.fuzzifikasi_input(nilai_input)

    # Terapkan aturan fuzzy
    himpunan_fuzzy_output = pengendali_fuzzy.terapkan_aturan(nilai_fuzzy_input)

    # Defuzzifikasi output
    nilai_tegas_output = pengendali_fuzzy.defuzzifikasi_output(himpunan_fuzzy_output)

    # Menampilkan hasil dalam bentuk tabel
    hasil_df = pd.DataFrame.from_dict(nilai_tegas_output, orient='index', columns=['Nilai Tegas Output'])

halaman_utama()
