# import xmlrpc bagian client saja
import xmlrpc.client
import os
import time

# buat stub (proxy) untuk client
s = xmlrpc.client.ServerProxy('http://127.0.0.1:8000', allow_none=True)


def clearTerminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def headerMenuRegistrasi():
    print("Registrasi Antrean Medis : \n")
    print("List Rumah Sakit beserta jumlah antriannya : \n")
    print(s.get_queue_size())


def menuRegistrasi():
    headerMenuRegistrasi()
    regisChoice = input("Apakah anda sudah pernah mendaftar (y/n)? ")
    data = {}
    if regisChoice == "y":
        clearTerminal()
        headerMenuRegistrasi()
        no_rekam_medis = input("Masukkan Nomor Rekam Medis : ")
        while no_rekam_medis == "":
            no_rekam_medis = input(
                "(input anda kosong) Masukkan Nomor Rekam Medis : ")
        poliklinik = input("Masukkan Pilihan RS : ")
        while poliklinik == "":
            poliklinik = input(
                "(input anda kosong) Masukkan Pilihan RS : ")
        data = {
            "no_rekam_medis": no_rekam_medis,
            "selected_rs": poliklinik
        }
    elif regisChoice == "n":
        clearTerminal()
        headerMenuRegistrasi()
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
    else:
        print("Input anda salah")
        time.sleep(1)
        clearTerminal()
        menuRegistrasi()
    print(s.registrasi(data))
    time.sleep(1)
    clearTerminal()
    return data


def mainMenu():
    print("Registrasi Antrean Medis : \n")
    if currentUser != None:
        print(currentUser["antrian"] + "\n")

    print("List Menu : \n")
    print("1. Registrasi")
    print("2. Cek Antrian di Setiap RS")
    print("3. Cek Akun")
    print("0. EXIT")
    return input("Pilih Menu (inputkan nomor menu) : ")


clearTerminal()
currentUser = None
while True:
    clearTerminal()
    menuChoice = mainMenu()
    if menuChoice == "1":
        clearTerminal()
        currentUser = menuRegistrasi()
        currentUser = s.get_user_object(currentUser["no_rekam_medis"])
        continue

    if menuChoice == "2":
        clearTerminal()
        print("Registrasi Antrean Medis : \n")
        print("daftar jumlah antrian di setiap RS : \n")
        print(s.get_queue_size())
        input("\nTekan Enter untuk kembali ke menu utama")
        continue

    if menuChoice == "3":
        clearTerminal()
        print("Registrasi Antrean Medis : \n")
        noRekamMedis = input("Masukkan Nomor Rekam Medis : ")
        print(s.get_detail_user(noRekamMedis))
        input("\nTekan Enter untuk kembali ke menu utama")
        continue

    if menuChoice == "0":
        clearTerminal()
        break
