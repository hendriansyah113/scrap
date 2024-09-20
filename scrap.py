import requests
import pandas as pd

# Membuat sesi request
session = requests.Session()

# Atur headers untuk sesi tersebut
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'Referer': 'https://sscasn.bkn.go.id',
    'Origin': 'https://sscasn.bkn.go.id'
})

base_url = 'https://api-sscasn.bkn.go.id/2024/portal/spf'
kode_ref_pend = '5101201'
offset = 0
all_data = []

while True:
    params = {
        'kode_ref_pend': kode_ref_pend,
        'offset': offset
    }

    # Mengirim permintaan GET ke API dengan sesi yang telah diatur
    response = session.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        
        # Pastikan kita mengambil data yang benar dari struktur JSON
        if 'data' in data and 'data' in data['data']:
            formasi_data = data['data']['data']
            if formasi_data:
                all_data.extend(formasi_data)
                offset += len(formasi_data)
            else:
                break
        else:
            print("Data tidak ditemukan dalam respon JSON.")
            break
    else:
        print(f"Gagal mengambil data, status code: {response.status_code}")
        break

print(f"Jumlah total data yang diambil: {len(all_data)}")

# Membuat DataFrame dan menyimpan ke Excel
df = pd.DataFrame(all_data)
file_path = 'C:/xampp/htdocs/surat/data_formasi.xlsx'
df.to_excel(file_path, index=False)
print(f"Data berhasil disimpan ke {file_path}")
