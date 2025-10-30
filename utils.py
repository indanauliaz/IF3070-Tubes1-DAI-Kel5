import json

# parsing json

def load_data(json_file):
    with open(json_file, 'r') as f:
        file_data = json.load(f)
    
    kapasitas = file_data['kapasitas_kontainer']
    list_barang_awal = file_data['barang']
    
    data_barang = {brg['id']: brg['ukuran'] for brg in list_barang_awal}
    
    return kapasitas, data_barang, list_barang_awal