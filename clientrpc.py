# import xmlrpc bagian client saja
import xmlrpc.client
import os
import time

# buat stub (proxy) untuk client
s = xmlrpc.client.ServerProxy(
    'https://3e10-36-65-206-127.ngrok.io', allow_none=True)


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
        tanggal_lahir = input("Masukkan Tanggal Lahir : ")
        nama = input("Masukkan Nama : ")
        poliklinik = input("Masukkan Pilihan RS : ")
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

    result = s.registrasi(data)

    print(result["antrian"])
    time.sleep(1)
    clearTerminal()
    return result


def mainMenu():
    print("Registrasi Antrean Medis : \n")
    if currentUser != None:
        print("Selamat datang, " + currentUser["nama"])
        print("No Rekam Medis anda : " + currentUser["no_rekam_medis"])
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
        result = menuRegistrasi()
        currentUser = s.get_user_object(result["no_rekam_medis"])
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
