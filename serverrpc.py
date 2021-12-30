# import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCServer

# import SimpleXMLRPCRequestHandler
from xmlrpc.server import SimpleXMLRPCRequestHandler
import threading

import datetime
import queue

# Antrean Registrasi Medis Membantu pasien agar tidak harus menunggu lama di rumah sakit saat antre ke klinik tertentu di rumah sakit.
# Client dapat melakukan registrasi (nomor rekam medis, nama, dan tanggal lahir) ke klinik tertentu di rumah sakit, dan mendapatkan nomor antrean.
# Server akan  mengirimkan  informasi  ke client berupa  data  antrean  saat  ini  dan perkiraan waktu kapan antrean client mendapatkan giliran.
# Client dapat melihat daftar klinik yang buka serta memilih salah satu klinik.

import threading


def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


DATABASE = {
    "RS": {
        '1': {
            "nama": "RS. Dr. Elang",
            "alamat": "Jl. Raya Cikarang",
            "queue": queue.Queue(10),
        },
        '2': {
            "nama": "RS. Dr. Agus",
            "alamat": "Jl. Raya Buah Batu",
            "queue": queue.Queue(10),
        },
        '3': {
            "nama": "RS. Dr. Faishal",
            "alamat": "Jl. Raya Serang",
            "queue": queue.Queue(10),
        },
    },
    "user": {
        '1': {
            "nama": "Agus",
            "tanggal_lahir": "12-12-2000",
            "no_rekam_medis": '1',
            "antrian": ''
        },
    }
}

WAKTU_ANTRIAN = 1


def dequeueIfExist():
    for _, value in DATABASE["RS"].items():
        if not value["queue"].empty():
            value["queue"].get()


# Batasi hanya pada path /RPC2 saja supaya tidak bisa mengakses path lainnya


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2')


# # Buat server
with SimpleXMLRPCServer(("127.0.0.1", 8000),
                        requestHandler=RequestHandler, allow_none=True) as server:

    # buat fungsi bernama registrasi()
    def registrasi(dataRegis):
        currentUser = None
        selected_rs = dataRegis["selected_rs"]
        if dataRegis["no_rekam_medis"] is None:
            dataRegis["no_rekam_medis"] = str(len(DATABASE["user"]) + 1)
            del dataRegis["selected_rs"]
            DATABASE["user"][dataRegis["no_rekam_medis"]] = dataRegis
            currentUser = dataRegis
        elif dataRegis["no_rekam_medis"] in DATABASE["user"].keys():
            currentUser = DATABASE["user"][dataRegis["no_rekam_medis"]]
        else:
            return "\nERROR : User tidak ditemukan\n"

        if selected_rs in DATABASE["RS"].keys():
            rs = DATABASE["RS"][selected_rs]
        else:
            return "\nERROR : RS tidak ditemukan\n"

        rs["queue"].put(currentUser)
        now = datetime.datetime.now()
        now_plus = now + \
            datetime.timedelta(minutes=WAKTU_ANTRIAN * rs['queue'].qsize())
        now_plus_formated = now_plus.strftime("%H:%M:%S")

        currentUser["antrian"] = f"Sekarang anda sendang mengantri pada {rs['nama']} dengan nomor antrian {rs['queue'].qsize()}. Estimasi {now_plus_formated}"
        DATABASE["user"][currentUser["no_rekam_medis"]] = currentUser
        print(DATABASE["user"][currentUser["no_rekam_medis"]])
        return f"Antrian kamu di {rs['nama']} sudah terdaftar. Nomor Antrian {rs['queue'].qsize()}. Estimasi {now_plus_formated}. (Nomor Rekam Medis anda adalah {currentUser['no_rekam_medis']})"

    def get_queue_size():
        rs_text = ""
        for idx, value in DATABASE["RS"].items():
            rs_text += f"{idx}. {value['nama']} : \nJumlah Antrian {value['queue'].qsize()}\n\n"
        return rs_text

    def get_user_object(no_rekam_medis):
        if no_rekam_medis in DATABASE["user"].keys():
            return DATABASE["user"][no_rekam_medis]
        else:
            return None

    def get_detail_user(no_rekam_medis):
        if no_rekam_medis in DATABASE["user"].keys():
            user = DATABASE["user"][no_rekam_medis]
            return f"Nama : {user['nama']}\nTanggal Lahir : {user['tanggal_lahir']}\nNomor Rekam Medis : {user['no_rekam_medis']}"
        else:
            return "\nERROR : User tidak ditemukan\n"

    def get_list_rs():
        rs_text = ""
        for key, value in DATABASE["RS"].items():
            rs_text += f"{key}. {value['nama']} \n"
        return rs_text

    # register fungsi ke rpc
    server.register_function(registrasi, 'registrasi')
    server.register_function(get_queue_size, 'get_queue_size')
    server.register_function(get_detail_user, 'get_detail_user')
    server.register_function(get_list_rs, 'get_list_rs')
    server.register_function(get_user_object, 'get_user_object')

    # Jalankan server
    print("Server Registrasi Medis berjalan...")
    server.serve_forever()
