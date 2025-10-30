import math
import random
import time
import utils
import matplotlib.pyplot as plt

CONTAINER_CAPACITY, DATA_BARANG, _ = utils.load_data('data_bin_packing.json')

# Parameter Objective Function
OVERFLOW_PENALTY = 10**4
DENSITY_ALPHA = 1.0
BIN_COUNT_FACTOR = 100

# Parameter Simulated Annealing
TEMP_START = 100.0
COOLING_RATE = 0.99999
MAX_ITER = 100

class BinPackingSA:
    def __init__(self, containers):
        self.containers = containers
        self.item_data = DATA_BARANG

    def get_container_size(self, container_index):
    
        total = 0
        for item_id in self.containers[container_index]:
            total += self.item_data.get(item_id, 0)
        return total

    def __len__(self):
        return len(self.containers)
    
    def copy(self):
        return BinPackingSA([list(c) for c in self.containers])

def first_fit(): # Metode heuristic first fit untuk penentuan state awal
    items = list(DATA_BARANG.items())
    random.shuffle(items) 
    containers = []

    for item_id, size in items:
        placed = False
        for c_idx in range(len(containers)):
            current_size = sum(DATA_BARANG[i] for i in containers[c_idx])
            if current_size + size <= CONTAINER_CAPACITY:
                containers[c_idx].append(item_id)
                placed = True
                break
        
        if not placed:
            containers.append([item_id])
            
    return BinPackingSA(containers)

def objective_function(state: BinPackingSA):
    invalid_penalti = 0
    for i in range(len(state)):
        total_size = state.get_container_size(i)
        if total_size > CONTAINER_CAPACITY:
            invalid_penalti += (total_size - CONTAINER_CAPACITY) * OVERFLOW_PENALTY

    skor1 = len(state) * BIN_COUNT_FACTOR
    skor2 = 0
    
    for i in range(len(state)):
        total_size = state.get_container_size(i)
        sisa_kapasitas = CONTAINER_CAPACITY - total_size
        skor2 += sisa_kapasitas * DENSITY_ALPHA 

    f_total = skor1 + skor2 + invalid_penalti
    return f_total

def generate_neighbor(state: BinPackingSA):
    state_next = state.copy() 
    if len(state_next) == 0:
        return state_next
        
    all_items = [(c_idx, item_id) for c_idx, c in enumerate(state_next.containers) for item_id in c]
    
    if not all_items:
        return state_next

    if random.random() < 0.5:
        from_container_idx, item_id = random.choice(all_items)
        state_next.containers[from_container_idx].remove(item_id)

        if random.random() < 0.8 and len(state_next) > 0: 
            to_container_idx = random.randrange(len(state_next))
        else:
            state_next.containers.append([])
            to_container_idx = len(state_next) - 1
            
        state_next.containers[to_container_idx].append(item_id)

    else:
        if len(state_next) < 2 or len(all_items) < 2:
            return state_next

        item1_loc, item2_loc = random.sample(all_items, 2)
        idx1, item1 = item1_loc
        idx2, item2 = item2_loc
        
        if idx1 != idx2:
            state_next.containers[idx1].remove(item1)
            state_next.containers[idx2].remove(item2)
            state_next.containers[idx1].append(item2)
            state_next.containers[idx2].append(item1)
        
    state_next.containers = [c for c in state_next.containers if c]
    return state_next

def simulated_annealing(state_initial: BinPackingSA, temp_start, cooling_rate, max_iter):
    state_current = state_initial.copy()
    temp_current = temp_start
    f_current = objective_function(state_current)
    
    state_best = state_current.copy()
    f_best = f_current
    
    history = [] 
    accepted_worse_moves = 0 

    start_time = time.time()
    
    for iterasi in range(1, max_iter + 1):
        state_next = generate_neighbor(state_current)
        f_next = objective_function(state_next)
        delta_E = f_next - f_current
        
        prob_acceptance = 0.0
        is_accepted = False
        
        if delta_E < 0:
            is_accepted = True
            prob_acceptance = 1.0
        elif temp_current > 0:
            prob_acceptance = math.exp(-delta_E / temp_current)
            if random.random() < prob_acceptance:
                is_accepted = True
                accepted_worse_moves += 1
                
        if is_accepted:
            state_current = state_next
            f_current = f_next
                
        if f_next < f_best:
             state_best = state_next.copy()
             f_best = f_next
        elif f_current < f_best: 
            state_best = state_current.copy()
            f_best = f_current
        
        temp_current *= cooling_rate

        history.append({
            'iterasi': iterasi,
            'f_current': f_current,
            'f_best_so_far': f_best,
            'T': temp_current,
            'Prob_Acceptance': prob_acceptance
        })
        
    end_time = time.time()
    durasi = end_time - start_time 

    return state_best, f_best, durasi, history, accepted_worse_moves

def print_state(state: BinPackingSA, state_name):    
    print(f"\n--- {state_name} ({len(state)} Kontainer) ---")
    
    for i, container in enumerate(state.containers):
        total_size = state.get_container_size(i)
        
        # Menampilkan status validity jika over capacity
        status = "OK"
        if total_size > CONTAINER_CAPACITY:
            status = "OVERLOAD!"

        item_details = [f"{item_id} ({state.item_data.get(item_id, '?')})" for item_id in container]
        print(f"Kontainer {i+1} [{status}]: Total = {total_size}/{CONTAINER_CAPACITY}. Barang: {', '.join(item_details)}")

    print(f"Objective Function Score: {objective_function(state):.4f}")
    
def plot_sa(history_data, run_id):
    iterasi = [d['iterasi'] for d in history_data]
    f_current = [d['f_current'] for d in history_data]
    f_best_so_far = [d['f_best_so_far'] for d in history_data]
    prob_acceptance = [d['Prob_Acceptance'] for d in history_data]
    temp_data = [d['T'] for d in history_data]
    
    fig, axes = plt.subplots(2, 1, figsize=(12, 10))
    fig.suptitle(f'Hasil Simulated Annealing (Run {run_id})', fontsize=16)

    # Plot 1: Objective Function vs. Iterasi
    axes[0].plot(iterasi, f_current, label='f(S) Current', alpha=0.6)
    axes[0].plot(iterasi, f_best_so_far, label='f(S) Terbaik', color='red', linewidth=2)
    axes[0].set_ylabel('Nilai Objective Function')
    axes[0].set_title('Plot Nilai Objective Function terhadap Iterasi')
    axes[0].legend()
    axes[0].grid(True, linestyle='--')
    
    # Plot 2: Probabilitas Penerimaan vs. Iterasi
    axes[1].plot(iterasi, prob_acceptance, label='Probabilitas Penerimaan', alpha=0.5)
    axes[1].set_xlabel('Iterasi')
    axes[1].set_ylabel('Nilai ($e^{-\Delta E / T}$)')
    axes[1].set_title('Plot ($e^{-\Delta E / T}$) terhadap Iterasi')

    ax2_twin = axes[1].twinx()
    ax2_twin.plot(iterasi, temp_data, label='Suhu (T)', color='red', linestyle=':')
    ax2_twin.set_ylabel('Suhu (T)')
    ax2_twin.legend(loc='upper right')
    
    axes[1].grid(True, linestyle='--')
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()
    
'''----- EKSEKUSI UTAMA -----
   program dijalankan tiga kali'''
if __name__ == "__main__":
    
    for run in range(1, 4):
        print(f"\n==================== EKSPERIMEN RUN {run} ====================")
    
        state_initial = first_fit()
        print_state(state_initial, "State Awal")
        
        best_solution, final_f_best, duration, history_data, stuck_counter = simulated_annealing(
            state_initial.copy(), TEMP_START, COOLING_RATE, MAX_ITER
        )
        
        print("\n--- Ringkasan Hasil ---")
        print(f"Objective Function Awal: {objective_function(state_initial):.4f}")
        print(f"Objective Function Akhir: {final_f_best:.4f}")
        print(f"Total Kontainer Digunakan: {len(best_solution)}")
        print(f"Durasi Proses Pencarian: {duration:.4f} detik")
        print(f"Total Move Buruk Diterima (Frekuensi Stuck): {stuck_counter}")
        print(f"Rasio Penerimaan Move Buruk: {stuck_counter / MAX_ITER:.4f}")

        print_state(best_solution, "State Akhir (Terbaik)")

        plot_sa(history_data, run)
