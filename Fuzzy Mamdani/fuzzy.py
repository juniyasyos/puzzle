import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Inisialisasi variabel input
variables = ['kain', 'malam', 'pewarna', 'biaya_produksi', 'permintaan', 'stok']

universe = np.arange(0, 101, 1)

input_variables = {var: ctrl.Antecedent(universe, var) for var in variables}
output_variable = ctrl.Consequent(universe, 'jumlah_produksi')

# Membership function untuk variabel input dan output
names = ['sedikit', 'sedang', 'banyak']
for var in input_variables.values():
    var.automf(3, names=names)

output_variable['sedikit'] = fuzz.trimf(output_variable.universe, [0, 30, 60])
output_variable['sedang'] = fuzz.trimf(output_variable.universe, [40, 70, 100])
output_variable['banyak'] = fuzz.trimf(output_variable.universe, [70, 100, 100])

# Membuat aturan menggunakan pendekatan lebih efisien
rules = []
for i in names:
    for j in names:
        for k in names:
            for l in names:
                for m in names:
                    for n in names:
                        for o in names:
                            antecedent = ctrl.Rule(
                                input_variables['kain'][i] & input_variables['malam'][j] & input_variables['pewarna'][k] &
                                input_variables['biaya_produksi'][l] & input_variables['permintaan'][m] & input_variables['stok'][n],
                                output_variable[o]
                            )
                            rules.append(antecedent)

# Membuat kontrol sistem fuzzy
jumlah_produksi_ctrl = ctrl.ControlSystem(rules)
jumlah_produksi_sim = ctrl.ControlSystemSimulation(jumlah_produksi_ctrl)

# Memberikan input
input_values = {'kain': 20, 'malam': 30, 'pewarna': 40, 'biaya_produksi': 10, 'permintaan': 50, 'stok': 70}
for var, val in input_values.items():
    jumlah_produksi_sim.input[var] = val

# Melakukan perhitungan
jumlah_produksi_sim.compute()

# Menampilkan hasil
print(jumlah_produksi_sim.output['jumlah_produksi'])

# Plot fungsi keanggotaan (opsional)
for var in input_variables.values():
    var.view()
output_variable.view()

input()
