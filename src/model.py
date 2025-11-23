class Pasien:
    def __init__(self, nama, nik, keluhan, kategori="Umum"):
        # --- PENERAPAN MODUL 5: Constructor ---
        self.nama = nama
        # --- PENERAPAN MODUL 6: Encapsulation (Private Attribute) ---
        self.__nik = nik  # Ada tanda __ (underscore 2x) artinya private
        self.keluhan = keluhan
        self.kategori = kategori

    # --- PENERAPAN MODUL 6: Getter Method ---
    # Kita butuh ini buat baca NIK, karena __nik itu private
    def get_nik(self):
        return self.__nik

    def info_lengkap(self):
        return f"Nama: {self.nama} | Kategori: {self.kategori} | Keluhan: {self.keluhan}"