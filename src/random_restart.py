import utils
import hc_utils
import time
import copy
import matplotlib.pyplot as plt

file_data = "data_bin_packing.json"
MAX_RESTARTS = 10 

print(f"Akan menjalankan pencarian sebanyak {MAX_RESTARTS} kali restart.")

kapasitas, data_barang, list_barang_awal = utils.load_data(file_data)

def run_steepest_ascent_inner_loop(start_state, kapasitas, data_barang):
    current_state = copy.deepcopy(start_state)
    current_score = hc_utils.calculate_objective(current_state, kapasitas, data_barang)
    
    skor_history = [current_score]
    iterasi = 0
    berhenti = False
    
    while not berhenti:
        iterasi += 1
        
        best_neighbor_state = None
        best_neighbor_score = float('inf') 
        
        neighbor_generator = hc_utils.get_neighbors(current_state)
        for neighbor in neighbor_generator:
            neighbor_score = hc_utils.calculate_objective(neighbor, kapasitas, data_barang)
            if neighbor_score < best_neighbor_score:
                best_neighbor_score = neighbor_score
                best_neighbor_state = neighbor
                
        if best_neighbor_state is None:
            berhenti = True
        elif best_neighbor_score < current_score:
            current_state = best_neighbor_state
            current_score = best_neighbor_score
            skor_history.append(current_score)
        else:
            skor_history.append(current_score) 
            berhenti = True
            
    return current_state, current_score, skor_history, iterasi

start_time = time.time()

global_best_score = float('inf')
global_best_final_state = None
global_best_skor_history = []   

first_run_initial_state = None
first_run_initial_score = 0

list_iterasi_per_restart = [] 
skor_history_gabungan = []    

for r in range(MAX_RESTARTS):
    print(f"\nRestart ke-{r+1}/{MAX_RESTARTS}")
    
    initial_state_random = hc_utils.inisialisasi_random(list_barang_awal, kapasitas, data_barang)
    initial_score_random = hc_utils.calculate_objective(initial_state_random, kapasitas, data_barang)
    print(f"State awal acak: {len(initial_state_random)} kontainer, Skor: {initial_score_random:.2f}")

    if r == 0:
        first_run_initial_state = copy.deepcopy(initial_state_random)
        first_run_initial_score = initial_score_random

    final_state, final_score, skor_history, total_iterasi = \
        run_steepest_ascent_inner_loop(initial_state_random, kapasitas, data_barang)
    
    print(f"Selesai di iterasi ke-{total_iterasi}. Skor lokal optimum: {final_score:.2f}")
    
    list_iterasi_per_restart.append(total_iterasi)
    skor_history_gabungan.extend(skor_history) 
    
    if final_score < global_best_score:
        print(f"DITEMUKAN SOLUSI BARU TERBAIK! (Skor: {final_score:.2f})")
        global_best_score = final_score
        global_best_final_state = final_state
        global_best_skor_history = skor_history     
        
end_time = time.time()

print("Hasil akhir:")
print(f"Durasi Total: {end_time - start_time:.4f} detik")
print(f"Total Restart Dilakukan: {MAX_RESTARTS}")
print(f"Rata-rata Iterasi per Restart: {sum(list_iterasi_per_restart) / len(list_iterasi_per_restart):.2f}")

print("\nState Awal:")
hc_utils.print_state_terminal(first_run_initial_state, kapasitas, data_barang)
print(f"Nilai Objective Function: {first_run_initial_score:.4f}")

print("\nState Akhir:")
hc_utils.print_state_terminal(global_best_final_state, kapasitas, data_barang)
print(f"Skor Akhir Terbaik: {global_best_score}")

# Plot
print("\nMembuat plot skor (dari run terbaik)...")
try:
    plt.figure(figsize=(10, 6)) 
    plt.plot(global_best_skor_history)
    plt.title('Random Restart: Nilai Objective Function vs Iterasi (Run Terbaik)')
    plt.xlabel('Iterasi (dalam 1 run)')
    plt.ylabel('Nilai Objective Function')
    plt.grid(True)
    
    nama_file_plot = 'random_restart_plot_skor.png' 
    plt.savefig(nama_file_plot)
    print(f"Plot skor berhasil disimpan sebagai: {nama_file_plot}")
    plt.show() 

except Exception as e:
    print(f"Gagal membuat plot skor: {e}")

print("\nMembuat plot analisis (iterasi per restart)...")
try:
    plt.figure(figsize=(10, 6))
    restart_labels = [f"R{i+1}" for i in range(MAX_RESTARTS)]
    plt.bar(restart_labels, list_iterasi_per_restart, color='coral')
    plt.title('Analisis Random Restart: Banyak Iterasi per Restart')
    plt.xlabel('Nomor Restart')
    plt.ylabel('Banyak Iterasi (sampai lokal optimum)')
    plt.bar_label(plt.gca().containers[0])
    
    nama_file_plot = 'random_restart_plot_analisis.png' 
    plt.savefig(nama_file_plot)
    print(f"Plot analisis berhasil disimpan sebagai: {nama_file_plot}")
    plt.show() 

except Exception as e:
    print(f"Gagal membuat plot analisis: {e}")

print("\nMembuat plot gabungan...")
try:
    plt.figure(figsize=(15, 6))
    plt.plot(skor_history_gabungan, linestyle='-', linewidth=0.8)
    plt.title('Analisis Random Restart: Plot Gabungan')
    plt.xlabel('Total Iterasi Gabungan (dari semua restart)')
    plt.ylabel('Nilai Objective Function')
    plt.grid(True, linestyle=':', alpha=0.7)
    
    nama_file_plot = 'random_restart_plot_gabungan.png' 
    plt.savefig(nama_file_plot)
    print(f"Plot gabungan berhasil disimpan sebagai: {nama_file_plot}")
    plt.show() 

except Exception as e:
    print(f"Gagal membuat plot gabungan: {e}")

print("\nMembuat plot konvergensi (Best vs Iterasi)...")
try:
    best_so_far_list = []
    current_best = float('inf')
    
    for score in skor_history_gabungan:
        if score < current_best:
            current_best = score
        best_so_far_list.append(current_best)
        
    plt.figure(figsize=(15, 6))
    plt.plot(best_so_far_list, linestyle='-', linewidth=1.5, color='blue', 
             label='Best Objective Function Value', drawstyle='steps-post')
    
    plt.title('Random Restart: Best Score vs Total Iterasi (Konvergensi)')
    plt.xlabel('Total Iterasi Gabungan (dari semua restart)')
    plt.ylabel('Best Objective Function Value')
    plt.grid(True)
    plt.legend()
    
    nama_file_plot = 'random_restart_plot_konvergensi.png' 
    plt.savefig(nama_file_plot)
    print(f"Plot berhasil disimpan sebagai: {nama_file_plot}")
    plt.show() 

except Exception as e:
    print(f"Gagal membuat plot 'konvergensi': {e}")