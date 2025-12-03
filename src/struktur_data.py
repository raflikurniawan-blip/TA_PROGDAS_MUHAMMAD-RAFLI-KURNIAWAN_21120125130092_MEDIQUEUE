from collections import deque

class KlinikManager:
    def __init__(self):
        self.antrian_darurat = deque()  
        self.antrian_umum = deque()     
        self.riwayat_panggilan = []

    @property
    def antrian_pasien(self):
        return list(self.antrian_darurat) + list(self.antrian_umum)

    def tambah_antrian(self, pasien):
        if pasien.kategori == "Darurat":
            self.antrian_darurat.append(pasien)
            print(f"[Sistem] Pasien DARURAT {pasien.nama} masuk antrian prioritas.")
        else:
            self.antrian_umum.append(pasien)
            print(f"[Sistem] Pasien {pasien.nama} masuk antrian umum.")

    def panggil_pasien(self):
        pasien_keluar = None
        if len(self.antrian_darurat) > 0:
            pasien_keluar = self.antrian_darurat.popleft()
            print(f"[Sistem] Memanggil pasien DARURAT: {pasien_keluar.nama}")
        
        elif len(self.antrian_umum) > 0:
            pasien_keluar = self.antrian_umum.popleft()
            print(f"[Sistem] Memanggil pasien UMUM: {pasien_keluar.nama}")
        
        if pasien_keluar:
            self.riwayat_panggilan.append(pasien_keluar)
            return pasien_keluar
        else:
            print("[Sistem] Antrian kosong!")
            return None

    def lihat_riwayat_terakhir(self):
        if len(self.riwayat_panggilan) > 0:
            return self.riwayat_panggilan[-1]
        else:
            return None
    
    def lihat_semua_riwayat(self):
        return self.riwayat_panggilan