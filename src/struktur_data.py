from collections import deque

class KlinikManager:
    def __init__(self):
        # --- PENERAPAN MODUL 7: QUEUE (FIFO) ---
        # Menggunakan deque biar proses antrian cepat
        self.antrian_pasien = deque()
        
        # --- PENERAPAN MODUL 7: STACK (LIFO) ---
        # Menggunakan list biasa sebagai tumpukan riwayat
        self.riwayat_panggilan = []

    def tambah_antrian(self, pasien):
        # Enqueue: Masuk dari belakang
        self.antrian_pasien.append(pasien)
        print(f"[Sistem] Pasien {pasien.nama} berhasil masuk antrian.")

    def panggil_pasien(self):
        # Cek apakah antrian kosong? (Modul 2: Pengkondisian)
        if len(self.antrian_pasien) > 0:
            # Dequeue: Keluar dari depan (FIFO)
            pasien_keluar = self.antrian_pasien.popleft()
            
            # Push ke Stack Riwayat (LIFO)
            self.riwayat_panggilan.append(pasien_keluar)
            
            return pasien_keluar
        else:
            return None

    def lihat_riwayat_terakhir(self):
        # Peek Stack: Intip data paling atas tumpukan (LIFO)
        if len(self.riwayat_panggilan) > 0:
            return self.riwayat_panggilan[-1]
        else:
            return None