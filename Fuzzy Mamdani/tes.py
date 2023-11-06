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
        'Kelembapan': {
            'Rendah': (0, 30),
            'Normal': (20, 80),
            'Tinggi': (70, 100)
        },
        'Suhu': {
            'Rendah': (0, 20),
            'Normal': (15, 25),
            'Tinggi': (20, 40)
        }
    }

    variabel_output = {
        'Kecepatan Kipas Angin': {
            'Lambat': (0, 30),
            'Sedang': (20, 70),
            'Cepat': (50, 100)
        }
    }

    # Inisialisasi pengendali fuzzy Mamdani
    pengendali_fuzzy = PengendaliFuzzyMamdani(variabel_input, variabel_output)

    # Tambahkan aturan-aturan fuzzy
    pengendali_fuzzy.tambahkan_aturan([('Kelembapan', 'Rendah'), ('Suhu', 'Tinggi')], [('Kecepatan Kipas Angin', 'Cepat')])
    pengendali_fuzzy.tambahkan_aturan([('Kelembapan', 'Normal'), ('Suhu', 'Normal')], [('Kecepatan Kipas Angin', 'Sedang')])
    pengendali_fuzzy.tambahkan_aturan([('Kelembapan', 'Tinggi'), ('Suhu', 'Rendah')], [('Kecepatan Kipas Angin', 'Lambat')])

    # Masukkan nilai input
    nilai_input = {
        'Kelembapan': 20,
        'Suhu': 35
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
