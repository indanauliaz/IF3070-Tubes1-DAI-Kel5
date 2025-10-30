import copy
import random
import matplotlib.pyplot as plt

def get_total_ukuran(kontainer, data_barang):
    total = 0
    for id_barang in kontainer:
        total += data_barang[id_barang]
    return total

def inisialisasi_first_fit(list_barang_awal, kapasitas, data_barang):
    state_awal = [] 
    
    for barang in list_barang_awal:
        id_barang_baru = barang['id']
        ukuran_barang_baru = barang['ukuran']
        
        barang_sudah_ditempatkan = False
        
        for kontainer in state_awal:
            total_ukuran_saat_ini = get_total_ukuran(kontainer, data_barang)
            
            if total_ukuran_saat_ini + ukuran_barang_baru <= kapasitas:
                kontainer.append(id_barang_baru)
                barang_sudah_ditempatkan = True
                break
        
        if not barang_sudah_ditempatkan:
            kontainer_baru = [id_barang_baru]
            state_awal.append(kontainer_baru)
            
    return state_awal

def inisialisasi_random(list_barang_awal, kapasitas, data_barang):
    shuffled_list = copy.deepcopy(list_barang_awal)
    random.shuffle(shuffled_list)
    return inisialisasi_first_fit(shuffled_list, kapasitas, data_barang)

def calculate_objective(state, kapasitas, data_barang):
    PENALTI_OVERLOAD = 10000 
    FAKTOR_BOBOT_KONTAINER = 100 

    jumlah_kontainer = len(state)
    skor_total = jumlah_kontainer * FAKTOR_BOBOT_KONTAINER
    
    total_reward_kepadatan = 0
    
    for kontainer in state:
        if not kontainer:
            continue
            
        total_ukuran_kontainer = get_total_ukuran(kontainer, data_barang)
        
        if total_ukuran_kontainer > kapasitas:
            skor_total += PENALTI_OVERLOAD
        else:
            kepadatan = total_ukuran_kontainer / kapasitas
            total_reward_kepadatan += (kepadatan ** 2)

    skor_total -= total_reward_kepadatan
    
    return skor_total

def clean_empty_containers(state):
    return [kontainer for kontainer in state if kontainer]

def get_neighbors(current_state):
    num_containers = len(current_state)
    
    for i in range(num_containers):
        if not current_state[i]:
            continue
            
        for j in range(len(current_state[i])):
            for k in range(num_containers):
                if i == k:
                    continue
                
                neighbor_state = copy.deepcopy(current_state)
                barang_yg_dipindah = neighbor_state[i].pop(j)
                neighbor_state[k].append(barang_yg_dipindah)
                
                yield clean_empty_containers(neighbor_state)
            
            neighbor_state = copy.deepcopy(current_state)
            barang_yg_dipindah = neighbor_state[i].pop(j)
            neighbor_state.append([barang_yg_dipindah])
            
            yield clean_empty_containers(neighbor_state)

    for i in range(num_containers):
        for j in range(len(current_state[i])):
            for k in range(i + 1, num_containers): 
                for l in range(len(current_state[k])):
                    
                    neighbor_state = copy.deepcopy(current_state)
                    
                    barang1 = neighbor_state[i][j]
                    barang2 = neighbor_state[k][l]
                    neighbor_state[i][j] = barang2
                    neighbor_state[k][l] = barang1
                    
                    yield neighbor_state

def print_state_terminal(state, kapasitas, data_barang):
    print("-" * 40)
    
    sorted_state = sorted(state, key=lambda k: get_total_ukuran(k, data_barang), reverse=True)
    
    for i, kontainer in enumerate(sorted_state):
        total_usage = get_total_ukuran(kontainer, data_barang)
        items_str = ", ".join(kontainer)
        warning = ""
        if total_usage > kapasitas:
            warning = " <-- OVERLOAD!"
            
        print(f"Kontainer {i+1:2d} (Total: {total_usage:3d}/{kapasitas}) {warning}")
        print(f"  [{items_str}]")
        
    print("-" * 40)
    print(f"Total Kontainer Digunakan: {len(state)}")