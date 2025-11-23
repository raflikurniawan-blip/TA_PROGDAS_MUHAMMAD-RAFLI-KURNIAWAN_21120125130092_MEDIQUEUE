import customtkinter as ctk
from tkinter import messagebox
from PIL import Image  
from src.model import Pasien
from src.struktur_data import KlinikManager

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class MediQueueApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("MediQueue - Sistem Antrian Klinik")
        self.geometry("900x600")
        self.resizable(True, True)

        # --- [UPDATE] SETUP BACKGROUND IMAGE MELAR ---
        try:
            from PIL import Image
            # 1. Simpan gambar asli ke 'self' biar bisa diakses nanti
            self.bg_source = Image.open("assets/bg1.jpg")
            
            # 2. Bikin gambar awal
            self.bg_image = ctk.CTkImage(light_image=self.bg_source,
                                         dark_image=self.bg_source,
                                         size=(900, 600))
            
            # 3. Tempel Label (Pakai relwidth/relheight biar labelnya ngikutin window)
            self.bg_label = ctk.CTkLabel(self, text="", image=self.bg_image)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            
            # 4. PASANG PENGAWAS (BINDING)
            # Kalau window berubah ukuran, panggil fungsi 'resize_bg'
            self.bind("<Configure>", self.resize_bg)
            
        except Exception as e:
            print(f"Background error: {e}")    
        except Exception as e:
            print(f"Background tidak ditemukan: {e}")

        self.klinik = KlinikManager()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_kiri = ctk.CTkFrame(self, width=300, corner_radius=15, fg_color="#151515")
        self.frame_kiri.grid(row=0, column=0, sticky="nswe", padx=20, pady=20)
        try:
            my_image = ctk.CTkImage(light_image=Image.open("assets/logo2.png"),
                                    dark_image=Image.open("assets/logo2.png"),
                                    size=(300, 300)) 

            self.logo2_label = ctk.CTkLabel(self.frame_kiri, text="", image=my_image)
            self.logo2_label.pack(pady=(0, 0)) 
        except Exception as e:
            print(f"Error loading logo: {e}")

        self.label_judul = ctk.CTkLabel(self.frame_kiri, 
                                text="PENDAFTARAN PASIEN", 
                                font=("Arial", 20, "bold"),
                                text_color="#29B6F6")
        self.label_judul.pack(pady=(0, 20), padx=20)

        self.entry_nama = ctk.CTkEntry(self.frame_kiri, placeholder_text="Nama Pasien")
        self.entry_nama.pack(pady=10, padx=20, fill="x")

        self.entry_nik = ctk.CTkEntry(self.frame_kiri, placeholder_text="NIK (KTP)")
        self.entry_nik.pack(pady=10, padx=20, fill="x")

        self.entry_keluhan = ctk.CTkEntry(self.frame_kiri, placeholder_text="Keluhan Utama")
        self.entry_keluhan.pack(pady=10, padx=20, fill="x")

        self.entry_nama.bind("<Return>", self.aksi_daftar)
        self.entry_nik.bind("<Return>", self.aksi_daftar)
        self.entry_keluhan.bind("<Return>", self.aksi_daftar)

        self.btn_daftar = ctk.CTkButton(self.frame_kiri, text="Daftar Antrian", fg_color="green", command=self.aksi_daftar)
        self.btn_daftar.pack(pady=20, padx=20, fill="x")

        self.frame_kanan = ctk.CTkFrame(self, corner_radius=15, fg_color="#151515")
        self.frame_kanan.grid(row=0, column=1, sticky="nswe", padx=(0, 20), pady=20)

        self.label_antrian = ctk.CTkLabel(self.frame_kanan, text="DAFTAR ANTRIAN SAAT INI (Queue)", font=("Arial", 18, "bold"))
        self.label_antrian.pack(pady=(10, 10))

        self.textbox_antrian = ctk.CTkTextbox(self.frame_kanan, width=500, height=300,
                                              fg_color="#000000", 
                                              text_color="white",
                                              bg_color="transparent")
        self.textbox_antrian.pack(pady=10)
        self.textbox_antrian.configure(state="disabled") 

        self.frame_tombol = ctk.CTkFrame(self.frame_kanan, fg_color="transparent")
        self.frame_tombol.pack(pady=20, fill="x")

        self.btn_panggil = ctk.CTkButton(self.frame_tombol, text="Panggil Pasien (Dequeue)", height=50, command=self.aksi_panggil)
        self.btn_panggil.pack(side="left", expand=True, padx=10, fill="x")

        self.btn_riwayat = ctk.CTkButton(self.frame_tombol, text="Cek Riwayat (Stack)", height=50, fg_color="gray", command=self.aksi_lihat_riwayat)
        self.btn_riwayat.pack(side="right", expand=True, padx=10, fill="x")

    def update_tampilan_antrian(self):
        self.textbox_antrian.configure(state="normal") 
        self.textbox_antrian.delete("1.0", "end") 
        
        nomor = 1
        for pasien in self.klinik.antrian_pasien:
            info = f"{nomor}. {pasien.info_lengkap()}\n"
            self.textbox_antrian.insert("end", info)
            nomor += 1
        
        self.textbox_antrian.configure(state="disabled") 

    def aksi_daftar(self, event=None):
        nama = self.entry_nama.get()
        nik = self.entry_nik.get()
        keluhan = self.entry_keluhan.get()

        if nama == "" or nik == "":
            messagebox.showwarning("Peringatan", "Nama dan NIK tidak boleh kosong!")
            return

        pasien_baru = Pasien(nama, nik, keluhan)
        
        self.klinik.tambah_antrian(pasien_baru)
        
        self.update_tampilan_antrian()
        self.bersihkan_input()
        messagebox.showinfo("Sukses", f"Pasien {nama} berhasil masuk antrian.")

    def aksi_panggil(self):
        pasien = self.klinik.panggil_pasien()
        
        if pasien:
            self.update_tampilan_antrian()
            messagebox.showinfo("Panggilan", f"Silakan masuk ke ruang dokter:\n\n{pasien.nama}\nKeluhan: {pasien.keluhan}")
        else:
            messagebox.showerror("Error", "Antrian Kosong!")

    def aksi_lihat_riwayat(self):
        pasien = self.klinik.lihat_riwayat_terakhir()
        
        if pasien:
            messagebox.showinfo("Riwayat Terakhir (Stack)", f"Pasien terakhir dipanggil:\n{pasien.nama} ({pasien.get_nik()})")
        else:
            messagebox.showinfo("Info", "Belum ada pasien yang dipanggil.")

    def bersihkan_input(self):
        self.entry_nama.delete(0, "end")
        self.entry_nik.delete(0, "end")
        self.entry_keluhan.delete(0, "end")
    
    # --- FUNGSI SUPAYA GAMBAR MELAR OTOMATIS ---
    def resize_bg(self, event):
        # Cek: Apakah yang berubah ukuran itu Window Utama? (Bukan tombol/input)
        if event.widget == self:
            # Cek: Apakah ukurannya beda dari yg sekarang? (Biar gak berat)
            # Kita ambil ukuran baru dari event.width dan event.height
            
            # Bikin gambar baru dengan ukuran layar yang baru
            new_bg_image = ctk.CTkImage(light_image=self.bg_source,
                                        dark_image=self.bg_source,
                                        size=(event.width, event.height))
            
            # Update gambar di label
            self.bg_label.configure(image=new_bg_image)