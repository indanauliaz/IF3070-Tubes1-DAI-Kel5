# IF3070-Tubes1-DAI-Kel5
# Tugas Besar 1 IF3070: Bin Packing Problem dengan Local Search

## Deskripsi Proyek

Proyek ini merupakan implementasi berbagai algoritma **Local Search** dan **Metaheuristik** untuk menyelesaikan masalah optimasi **Bin Packing Problem (BPP)**.

Tujuan utamanya adalah menempatkan sekumpulan barang dengan ukuran berbeda ke dalam sejumlah kontainer (bins) dengan kapasitas yang sama, dengan objektif untuk **meminimalkan jumlah kontainer** yang digunakan.

Proyek ini dibuat untuk memenuhi Tugas Besar 1 mata kuliah **IF3070 Dasar Inteligensi Artifisial**.

## Anggota Kelompok

| Nama | NIM |
| :--- | :--- |
| Vincentia Belinda Sumartoyo | 18223078 |
| Indana Aulia Ayundazulfa | 18223100 |
| Nurul Na'im Natifah | 18223106 |

## Algoritma yang Diimplementasikan

Program ini mengimplementasikan beberapa algoritma untuk menyelesaikan BPP:

**1. Hill Climbing**
**2. Simulated Annealing**
**3. Genetic Algorithm**

## Cara Menjalankan Program

1.  Clone repositori ini:
    ```bash
    git clone [https://github.com/indanauliaz/IF3070-Tubes1-DAI-Kel5.git](https://github.com/indanauliaz/IF3070-Tubes1-DAI-Kel5.git)
    ```
2.  Masuk ke direktori proyek:
    ```bash
    cd IF3070-Tubes1-DAI-Kel5
    ```
3.  ```bash
    python [namafile].py
    ```

* `[namafile].py`: Ganti dengan nama file dari daftar di bawah ini:
    * `sahc.py` (Steepest Ascent Hill Climbing)
    * `shc.py` (Stochastic Hill Climbing)
    * `fchc.py` (First Choice Hill Climbing)
    * `rhc.py` (Random-Restart Hill Climbing)
    * `sa.py` (Simulated Annealing)
    * `ga.py` (Genetic Algorithm)