# import xmlrpc bagian client saja
import xmlrpc.client

# buat stub (proxy) untuk client
s = xmlrpc.client.ServerProxy('http://127.0.0.1:8000', allow_none=True)

# Lakukan Registrasi berdasarkan Poliklinik yang tersedia


print("Registrasi Medis (Pilih Poliklinik) : \n")
print(s.get_list_rs())
print("Apakah anda sudah pernah mendaftar ? (y/n)")
regisChoice = input()
data = {}
if regisChoice == "y":
    print("Masukkan Nomor Rekam Medis : ")
    no_rekam_medis = input()
    print("Masukkan Pilihan RS : ")
    poliklinik = input()
    data = {
        "no_rekam_medis": no_rekam_medis,
        "selected_rs": poliklinik
    }
else:
    print("Masukkan Tanggal Lahir : ")
    tanggal_lahir = input()
    print("Masukkan Nama : ")
    nama = input()
    print("Masukkan Pilihan RS : ")
    poliklinik = input()
    data = {
        "tanggal_lahir": tanggal_lahir,
        "nama": nama,
        "selected_rs": poliklinik,
        "no_rekam_medis": None
    }

print(s.registrasi(data))
