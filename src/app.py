import customtkinter as ctk
from tkinter import messagebox
from src.model import Pasien
from src.struktur_data import KlinikManager

# --- CONFIG TEMA ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class MediQueueApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 1. Setup Jendela Utama
        self.title("MediQueue - Sistem Antrian Klinik")
        self.geometry("900x600")
        self.resizable(False, False)

        # 2. Inisialisasi Backend (Otak Aplikasi)
        self.klinik = KlinikManager()

        # 3. Layouting (Grid System)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- PANEL KIRI (INPUT DATA) ---
        self.frame_kiri = ctk.CTkFrame(self, width=300, corner_radius=0)
        self.frame_kiri.grid(row=0, column=0, sticky="nswe")

        self.label_judul = ctk.CTkLabel(self.frame_kiri, text="PENDAFTARAN PASIEN", font=("Arial", 20, "bold"))
        self.label_judul.pack(pady=30, padx=20)

        self.entry_nama = ctk.CTkEntry(self.frame_kiri, placeholder_text="Nama Pasien")
        self.entry_nama.pack(pady=10, padx=20, fill="x")

        self.entry_nik = ctk.CTkEntry(self.frame_kiri, placeholder_text="NIK (KTP)")
        self.entry_nik.pack(pady=10, padx=20, fill="x")

        self.entry_keluhan = ctk.CTkEntry(self.frame_kiri, placeholder_text="Keluhan Utama")
        self.entry_keluhan.pack(pady=10, padx=20, fill="x")

        self.btn_daftar = ctk.CTkButton(self.frame_kiri, text="Daftar Antrian", fg_color="green", command=self.aksi_daftar)
        self.btn_daftar.pack(pady=20, padx=20, fill="x")

        # --- PANEL KANAN (MONITOR ANTRIAN) ---
        self.frame_kanan = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_kanan.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # Judul Kanan
        self.label_antrian = ctk.CTkLabel(self.frame_kanan, text="DAFTAR ANTRIAN SAAT INI (Queue)", font=("Arial", 18, "bold"))
        self.label_antrian.pack(pady=(10, 10))

        # Area Teks untuk Menampilkan Antrian (Scrollable)
        self.textbox_antrian = ctk.CTkTextbox(self.frame_kanan, width=500, height=300)
        self.textbox_antrian.pack(pady=10)
        self.textbox_antrian.configure(state="disabled") # Biar gak bisa diedit manual user

        # Tombol Kontrol
        self.frame_tombol = ctk.CTkFrame(self.frame_kanan, fg_color="transparent")
        self.frame_tombol.pack(pady=20, fill="x")

        self.btn_panggil = ctk.CTkButton(self.frame_tombol, text="Panggil Pasien (Dequeue)", height=50, command=self.aksi_panggil)
        self.btn_panggil.pack(side="left", expand=True, padx=10, fill="x")

        self.btn_riwayat = ctk.CTkButton(self.frame_tombol, text="Cek Riwayat (Stack)", height=50, fg_color="gray", command=self.aksi_lihat_riwayat)
        self.btn_riwayat.pack(side="right", expand=True, padx=10, fill="x")

    # --- LOGIKA INTERAKSI (Integrasi Modul 2, 4, 5, 6, 7) ---
    def update_tampilan_antrian(self):
        self.textbox_antrian.configure(state="normal") # Buka kunci
        self.textbox_antrian.delete("1.0", "end") # Hapus isi lama
        
        # Loop antrian dari Backend
        nomor = 1
        for pasien in self.klinik.antrian_pasien:
            info = f"{nomor}. {pasien.info_lengkap()}\n"
            self.textbox_antrian.insert("end", info)
            nomor += 1
        
        self.textbox_antrian.configure(state="disabled") # Kunci lagi

    def aksi_daftar(self):
        # Ambil input dari GUI
        nama = self.entry_nama.get()
        nik = self.entry_nik.get()
        keluhan = self.entry_keluhan.get()

        # Validasi Input (Modul 2: Pengkondisian)
        if nama == "" or nik == "":
            messagebox.showwarning("Peringatan", "Nama dan NIK tidak boleh kosong!")
            return

        # Buat Objek Pasien (Modul 5)
        pasien_baru = Pasien(nama, nik, keluhan)
        
        # Masukkan ke Backend (Modul 7 Enqueue)
        self.klinik.tambah_antrian(pasien_baru)
        
        # Update GUI
        self.update_tampilan_antrian()
        self.bersihkan_input()
        messagebox.showinfo("Sukses", f"Pasien {nama} berhasil masuk antrian.")

    def aksi_panggil(self):
        # Panggil Logic Backend (Modul 7 Dequeue)
        pasien = self.klinik.panggil_pasien()
        
        if pasien:
            self.update_tampilan_antrian()
            messagebox.showinfo("Panggilan", f"Silakan masuk ke ruang dokter:\n\n{pasien.nama}\nKeluhan: {pasien.keluhan}")
        else:
            messagebox.showerror("Error", "Antrian Kosong!")

    def aksi_lihat_riwayat(self):
        # Panggil Logic Backend (Modul 7 Stack Peek)
        pasien = self.klinik.lihat_riwayat_terakhir()
        
        if pasien:
            messagebox.showinfo("Riwayat Terakhir (Stack)", f"Pasien terakhir dipanggil:\n{pasien.nama} ({pasien.get_nik()})")
        else:
            messagebox.showinfo("Info", "Belum ada pasien yang dipanggil.")

    def bersihkan_input(self):
        self.entry_nama.delete(0, "end")
        self.entry_nik.delete(0, "end")
        self.entry_keluhan.delete(0, "end")