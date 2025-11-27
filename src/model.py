class Pasien:
    def __init__(self, nama, nik, keluhan, kategori="Umum"):
        self.nama = nama
        self.__nik = nik 
        self.keluhan = keluhan
        self.kategori = kategori 
        
    def get_nik(self):
        return self.__nik

    def info_lengkap(self):
        return f"[{self.kategori}] {self.nama} | Keluhan: {self.keluhan}"