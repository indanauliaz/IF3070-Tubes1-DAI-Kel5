import utils
import hc_utils
import time
import copy
import random
import matplotlib.pyplot as plt

file_data = "data_bin_packing.json"

print(f"Loading data dari {file_data}...")
kapasitas, data_barang, list_barang_awal = utils.load_data(file_data)

print("Inisialisasi state awal (First Fit)...")
initial_state = hc_utils.inisialisasi_first_fit(list_barang_awal, kapasitas, data_barang)
initial_score = hc_utils.calculate_objective(initial_state, kapasitas, data_barang)

print("\nState Awal:")
hc_utils.print_state_terminal(initial_state, kapasitas, data_barang)
print(f"Nilai Objective Function: {initial_score:.4f}")

print("\nMulai hill climbing (Stochastic)...")

current_state = copy.deepcopy(initial_state)
current_score = initial_score
skor_per_iterasi = [current_score]
iterasi = 0
start_time = time.time()

while True:
    iterasi += 1
    print(f"\nIterasi ke-{iterasi}")
    
    better_neighbors = []
    
    neighbor_generator = hc_utils.get_neighbors(current_state)
    
    for neighbor in neighbor_generator:
        neighbor_score = hc_utils.calculate_objective(neighbor, kapasitas, data_barang)
        
        if neighbor_score < current_score:
            better_neighbors.append((neighbor, neighbor_score))
            
    if not better_neighbors:
        print("Tidak ada solusi lebih baik, terjebak di local optimum.")
        skor_per_iterasi.append(current_score)
        break
    else:
        selected_neighbor, selected_score = random.choice(better_neighbors)
        
        current_state = selected_neighbor
        current_score = selected_score
        
        skor_per_iterasi.append(current_score)
        
        print(f"Ditemukan {len(better_neighbors)} tetangga lebih baik. Memilih 1 secara acak.")
        print(f"Skor membaik: {current_score:.4f} ({len(current_state)} kontainer)")

end_time = time.time()

print("\nHasil akhir:")
print(f"Durasi: {end_time - start_time:.4f} detik")
print(f"Banyak iterasi: {iterasi}")
print(f"State awal ({len(initial_state)} kontainer), nilai objective function = {initial_score:.4f}")
print(f"State akhir ({len(current_state)} kontainer), nilai objective function = {current_score:.4f}\n")

print("State Akhir:")
hc_utils.print_state_terminal(current_state, kapasitas, data_barang)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(skor_per_iterasi)
plt.title('Stochastic Hill Climbing: Nilai Objective Function vs Iterasi')
plt.xlabel('Iterasi')
plt.ylabel('Nilai Objective Function')
plt.grid(True)
plt.savefig('stochastic_hc_plot.png')
print(f"\nPlot disimpan sebagai stochastic_hc_plot.png")
plt.show()