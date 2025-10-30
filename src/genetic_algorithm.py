import random
import matplotlib.pyplot as plt
import utils
import time

class GenAlgo:
    def init_engine(self, data_barang, list_id, batas_kapasitas, jumlah_pop, total_gen, rasio_mutasi):
        # setup awal parameter
        self.data_barang = data_barang
        self.list_id = list_id
        self.batas_kapasitas = batas_kapasitas
        self.jumlah_pop = jumlah_pop
        self.total_gen = total_gen
        self.rasio_mutasi = rasio_mutasi
        self.jumlah_barang = len(list_id)
        self.populasi = []
        self.fitness_history = []

    def buat_populasi_awal(self):
        print("Membuat populasi awal...")
        for i in range(self.jumlah_pop):
            kromosom = []
            for j in range(self.jumlah_barang):
                # setiap barang ditempatkan di kontainer acak
                kromosom.append(random.randint(0, self.jumlah_barang - 1))
            self.populasi.append(kromosom)

    def hitung_fitness(self, kromosom):
        kontainer = {}
        penalti_over = 0
        reward_padat = 0

        # masukkan barang ke dalam kontainer sesuai kromosom
        for i in range(self.jumlah_barang):
            id_brg = self.list_id[i]
            ukuran = self.data_barang[id_brg]
            no_kontainer = kromosom[i]

            if no_kontainer not in kontainer:
                kontainer[no_kontainer] = 0
            kontainer[no_kontainer] += ukuran

        # hitung penalti overflow dan reward kepadatan
        for key in kontainer:
            isi = kontainer[key]
            if isi > self.batas_kapasitas:
                penalti_over += isi - self.batas_kapasitas
            else:
                kepadatan = isi / self.batas_kapasitas
                reward_padat += kepadatan ** 2

        # hitung total fitness
        penalti = 10000
        faktor_kontainer = 100
        total_kontainer = len(kontainer)
        fitness = (penalti_over * penalti) + (total_kontainer * faktor_kontainer) - reward_padat
        return fitness

    def pilih_parent(self):
        ukuran_turnamen = 5
        kandidat1 = random.sample(self.populasi, ukuran_turnamen)
        kandidat2 = random.sample(self.populasi, ukuran_turnamen)

        parent1 = min(kandidat1, key=lambda ind: self.hitung_fitness(ind))
        parent2 = min(kandidat2, key=lambda ind: self.hitung_fitness(ind))
        return parent1, parent2

    def crossover(self, parent1, parent2):
        titik = random.randint(1, self.jumlah_barang - 1)
        anak1 = parent1[:titik] + parent2[titik:]
        anak2 = parent2[:titik] + parent1[titik:]
        return anak1, anak2

    def mutasi(self, kromosom):
        hasil = list(kromosom)
        kontainer_unik = list(set(hasil))
        if len(kontainer_unik) == 0:
            return hasil

        # mutasi acak sebagian gen
        for i in range(self.jumlah_barang):
            if random.random() < self.rasio_mutasi:
                if random.random() < 0.5:
                    hasil[i] = random.choice(kontainer_unik)
                else:
                    hasil[i] = random.randint(0, self.jumlah_barang - 1)
        return hasil

    def jalankan(self):
        self.buat_populasi_awal()
        individu_awal = None

        for gen in range(self.total_gen):
            semua_fitness = []
            total_fit = 0
            terbaik = float("inf")
            individu_terbaik = None

            for kromosom in self.populasi:
                nilai_fit = self.hitung_fitness(kromosom)
                semua_fitness.append((nilai_fit, kromosom))
                total_fit += nilai_fit
                if nilai_fit < terbaik:
                    terbaik = nilai_fit
                    individu_terbaik = kromosom

            if gen == 0:
                individu_awal = individu_terbaik

            rata_fit = total_fit / self.jumlah_pop
            self.fitness_history.append((terbaik, rata_fit))

            if gen % 10 == 0:
                print(f"Generasi {gen}: Fitness terbaik = {terbaik}, Rata-rata = {rata_fit}")

            populasi_baru = []
            while len(populasi_baru) < self.jumlah_pop:
                parent1, parent2 = self.pilih_parent()
                c1, c2 = self.crossover(parent1, parent2)
                c1 = self.mutasi(c1)
                c2 = self.mutasi(c2)
                populasi_baru.extend([c1, c2])

            self.populasi = populasi_baru[:self.jumlah_pop]

        hasil_akhir = min([(self.hitung_fitness(k), k) for k in self.populasi], key=lambda x: x[0])
        print(f"Fitness terbaik: {hasil_akhir[0]}")
        return hasil_akhir[1], self.fitness_history, individu_awal


def tampilkan_solusi(individu, data_barang, list_id, kapasitas):
    wadah = {}
    for i in range(len(list_id)):
        idb = list_id[i]
        ukuran = data_barang[idb]
        bin_no = individu[i]
        if bin_no not in wadah:
            wadah[bin_no] = []
        wadah[bin_no].append((idb, ukuran))

    print(f"Total Kontainer: {len(wadah)}")
    for idx, key in enumerate(sorted(wadah.keys()), start=1):
        total = sum(x[1] for x in wadah[key])
        print(f"{idx}. Kontainer (Total: {total}/{kapasitas})")
        for brg in wadah[key]:
            print(f"   - {brg[0]} ({brg[1]})")


if __name__ == "__main__":
    file_data = "data_bin_packing.json"
    kapasitas, data_barang, _ = utils.load_data(file_data)
    list_id = list(data_barang.keys())

    POP = 50  # Populasi
    GEN = 100  # Generasi
    MUT = 1 # Probabilitas mutasi

    model = GenAlgo()
    model.init_engine(data_barang, list_id, kapasitas, POP, GEN, MUT)

    start = time.time()
    hasil, log_fit, awal = model.jalankan()
    end = time.time()

    print("\nGenerasi Awal")
    tampilkan_solusi(awal, data_barang, list_id, kapasitas)

    print("\nGenerasi Akhir")
    tampilkan_solusi(hasil, data_barang, list_id, kapasitas)

    durasi = end - start
    print(f"\nDurasi: {durasi:.2f} detik")

    # Plot
    log_fit_terbaik = [x[0] for x in log_fit]
    log_fit_rata = [x[1] for x in log_fit]
    fig, axes = plt.subplots(2, 1, figsize=(10, 8)) 

    axes[0].plot(log_fit_terbaik, label="Best Objective Function Value", color='blue')
    axes[0].set_title("Best Objective Function Value vs Iterations")
    axes[0].set_ylabel("Best Objective Value")
    axes[0].set_xlabel("Generation (Iteration)") 
    
    skor_valid = [s for s in log_fit_terbaik if s < 10000]
    
    if skor_valid:
        min_skor = min(skor_valid)
        max_skor = max(skor_valid)
        axes[0].set_ylim(min_skor - 100, max_skor + 100)
        
    axes[0].legend()
    axes[0].grid(True) 

    axes[1].plot(log_fit_rata, label="Average Objective Function Value", color='orange')
    axes[1].set_title("Average Objective Function Value vs Iterations")
    axes[1].set_xlabel("Generation (Iteration)") 
    axes[1].set_ylabel("Average Objective Function Value")
    axes[1].legend()
    axes[1].grid(True) 

    plt.tight_layout()
    plt.show()
