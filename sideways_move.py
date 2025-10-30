import utils
import hc_utils
import time
import copy
import matplotlib.pyplot as plt

file_data = "data_bin_packing.json"
MAX_SIDEWAYS_MOVES = 50 

print(f"Loading data dari {file_data}...")
kapasitas, data_barang, list_barang_awal = utils.load_data(file_data)

print("Inisialisasi state awal (First Fit)...")
initial_state = hc_utils.inisialisasi_first_fit(list_barang_awal, kapasitas, data_barang)
initial_score = hc_utils.calculate_objective(initial_state, kapasitas, data_barang)

print("\nState Awal:")
hc_utils.print_state_terminal(initial_state, kapasitas, data_barang)
print(f"Nilai Objective Function: {initial_score:.4f}")

print("\nMulai hill climbing (Sideways Move)...")

current_state = copy.deepcopy(initial_state)
current_score = initial_score
skor_per_iterasi = [current_score]
iterasi = 0
start_time = time.time()

sideways_moves_count = 0 

while True:
    iterasi += 1
    print(f"\nIterasi ke-{iterasi} (Sideways count: {sideways_moves_count}/{MAX_SIDEWAYS_MOVES})")

    best_state = None
    best_score = float('inf')

    for neighbor in hc_utils.get_neighbors(current_state):
        score = hc_utils.calculate_objective(neighbor, kapasitas, data_barang)
        if score < best_score:
            best_score = score
            best_state = neighbor

    if not best_state:
        print("Tidak ada tetangga yang bisa digenerate.")
        break

    if best_score < current_score:
        current_state = best_state
        current_score = best_score
        skor_per_iterasi.append(current_score)
        
        sideways_moves_count = 0 
        
        print(f"Skor membaik: {current_score:.4f} ({len(current_state)} kontainer)")
        
    elif best_score == current_score:
        if sideways_moves_count >= MAX_SIDEWAYS_MOVES:
            print(f"Batas sideways move ({MAX_SIDEWAYS_MOVES}) tercapai. Berhenti di dataran.")
            skor_per_iterasi.append(current_score)
            break 
        else:
            current_state = best_state
            current_score = best_score 
            skor_per_iterasi.append(current_score)
            
            sideways_moves_count += 1 
            
            print(f"Melakukan SIDEWAYS MOVE (Count: {sideways_moves_count}/{MAX_SIDEWAYS_MOVES}). Skor tetap.")
            
    else: 
        print("Tidak ada solusi lebih baik, terjebak di local optimum.")
        skor_per_iterasi.append(current_score)
        break 

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
plt.title('Hill Climbing with Sideways Move: Nilai Objective Function vs Iterasi')
plt.xlabel('Iterasi')
plt.ylabel('Nilai Objective Function') 
plt.grid(True)
plt.savefig('sideways_move_plot.png')
print("\nPlot disimpan sebagai sideways_move_plot.png")
plt.show()