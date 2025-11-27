import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from src.model import Pasien
from src.struktur_data import KlinikManager
from datetime import datetime

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class MediQueueApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("MediQueue - Sistem Antrian Klinik")
        self.geometry("1200x700")
        self.resizable(True, True)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        try:
            from PIL import Image
            self.bg_source = Image.open("assets/bg_klinik.jpg")
            self.bg_image = ctk.CTkImage(light_image=self.bg_source,
                                         dark_image=self.bg_source,
                                         size=(1200, 700))
            self.bg_label = ctk.CTkLabel(self, text="", image=self.bg_image)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.bind("<Configure>", self.resize_bg)
        except Exception as e:
            print(f"Background error: {e}")

        #init backend
        self.klinik = KlinikManager()

        #layout grid
        self.grid_columnconfigure(0, weight=0, minsize=350)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_kiri = ctk.CTkFrame(self, width=350, corner_radius=15, fg_color="#151515")
        self.frame_kiri.grid(row=0, column=0, sticky="nswe", padx=20, pady=20)

        try:
            my_image = ctk.CTkImage(light_image=Image.open("assets/logo.png"),
                                    dark_image=Image.open("assets/logo.png"),
                                    size=(150, 150))
            self.logo_label = ctk.CTkLabel(self.frame_kiri, text="", image=my_image)
            self.logo_label.pack(pady=(15, 0))
        except:
            pass  

        self.label_judul = ctk.CTkLabel(self.frame_kiri, text="PENDAFTARAN PASIEN",
                                      font=("Arial", 20, "bold"), text_color="#29B6F6")
        self.label_judul.pack(pady=(5, 15))

        self.label_nama = ctk.CTkLabel(self.frame_kiri, text="Nama Lengkap", 
                                       font=("Arial", 12), anchor="w")
        self.label_nama.pack(padx=20, anchor="w")
        self.entry_nama = ctk.CTkEntry(self.frame_kiri, placeholder_text="Contoh: Budi Santoso", 
                                       height=35, font=("Arial", 12))
        self.entry_nama.pack(pady=(0, 10), padx=20, fill="x")

        self.label_nik = ctk.CTkLabel(self.frame_kiri, text="NIK (16 Digit)", 
                                      font=("Arial", 12), anchor="w")
        self.label_nik.pack(padx=20, anchor="w")
        self.entry_nik = ctk.CTkEntry(self.frame_kiri, placeholder_text="Contoh: 3201234567890123", 
                                      height=35, font=("Arial", 12))
        self.entry_nik.pack(pady=(0, 10), padx=20, fill="x")

        self.label_keluhan = ctk.CTkLabel(self.frame_kiri, text="Keluhan Utama", 
                                          font=("Arial", 12), anchor="w")
        self.label_keluhan.pack(padx=20, anchor="w")
        self.entry_keluhan = ctk.CTkEntry(self.frame_kiri, placeholder_text="Contoh: Demam tinggi 3 hari", 
                                          height=35, font=("Arial", 12))
        self.entry_keluhan.pack(pady=(0, 10), padx=20, fill="x")

        self.label_kat = ctk.CTkLabel(self.frame_kiri, text="Kategori Pasien:", 
                                      font=("Arial", 12), anchor="w")
        self.label_kat.pack(padx=20, anchor="w")
        self.combo_kategori = ctk.CTkComboBox(self.frame_kiri, 
                                              values=["Umum", "Darurat"], 
                                              height=35,
                                              font=("Arial", 12))
        self.combo_kategori.pack(pady=(0, 20), padx=20, fill="x")
        self.combo_kategori.set("Umum")  

        self.btn_daftar = ctk.CTkButton(self.frame_kiri, text="DAFTAR ANTRIAN", 
                                      height=45,
                                      fg_color="#2ecc71",  
                                      hover_color="#27ae60",
                                      font=("Arial", 15, "bold"),
                                      command=self.aksi_daftar)
        self.btn_daftar.pack(pady=(0, 20), padx=20, fill="x")

        self.entry_nama.bind("<Return>", self.aksi_daftar)
        self.entry_nik.bind("<Return>", self.aksi_daftar)
        self.entry_keluhan.bind("<Return>", self.aksi_daftar)

        self.frame_kanan = ctk.CTkFrame(self, corner_radius=15, fg_color="#151515")
        self.frame_kanan.grid(row=0, column=1, sticky="nswe", padx=(0, 20), pady=20)

        #grid layout kanan 5 rows
        self.frame_kanan.grid_columnconfigure(0, weight=1)
        self.frame_kanan.grid_rowconfigure(2, weight=1)  #antrian
        self.frame_kanan.grid_rowconfigure(5, weight=1)  #riwayat

        #stats+jam       
        self.frame_header = ctk.CTkFrame(self.frame_kanan, fg_color="transparent")
        self.frame_header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))

        self.frame_jam = ctk.CTkFrame(self.frame_header, fg_color="transparent")
        self.frame_jam.pack(side="right")
        self.label_jam = ctk.CTkLabel(self.frame_jam, text="00:00:00", 
                                      font=("Arial", 32, "bold"), 
                                      text_color="#29B6F6")
        self.label_jam.pack(anchor="e")
        self.label_tgl = ctk.CTkLabel(self.frame_jam, text="Memuat...", 
                                      font=("Arial", 12))
        self.label_tgl.pack(anchor="e")

       #stats kiri
        self.frame_stats = ctk.CTkFrame(self.frame_header, fg_color="transparent")
        self.frame_stats.pack(side="left", fill="x", expand=True)
        self.lbl_stat_total = ctk.CTkLabel(self.frame_stats, text="Sisa Antrian: 0", 
                                           font=("Arial", 14, "bold"))
        self.lbl_stat_total.pack(anchor="w")
        self.lbl_stat_darurat = ctk.CTkLabel(self.frame_stats, text="Darurat: 0", 
                                             font=("Arial", 14, "bold"), 
                                             text_color="#e74c3c")
        self.lbl_stat_darurat.pack(anchor="w")

        self.label_q_title = ctk.CTkLabel(self.frame_kanan, text="DAFTAR ANTRIAN SAAT INI", 
                                          font=("Arial", 16, "bold"))
        self.label_q_title.grid(row=1, column=0, sticky="w", padx=20, pady=(10, 0))

        self.textbox_antrian = ctk.CTkTextbox(self.frame_kanan, 
                                              font=("Consolas", 14), 
                                              fg_color="#0d0d0d",
                                              text_color="white")
        self.textbox_antrian.grid(row=2, column=0, sticky="nswe", padx=20, pady=10)
        self.textbox_antrian.configure(state="disabled")  #read only

        self.frame_tombol = ctk.CTkFrame(self.frame_kanan, fg_color="transparent")
        self.frame_tombol.grid(row=3, column=0, sticky="ew", padx=20, pady=10)

        self.btn_panggil = ctk.CTkButton(self.frame_tombol, 
                                       text="PANGGIL PASIEN",
                                       height=50, 
                                       font=("Arial", 14, "bold"),
                                       fg_color="#3498db",
                                       hover_color="#2980b9",
                                       command=self.aksi_panggil)
        self.btn_panggil.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.btn_refresh = ctk.CTkButton(self.frame_tombol, 
                                       text="🔄", 
                                       width=50, 
                                       height=50,
                                       fg_color="#7f8c8d",
                                       hover_color="#95a5a6",
                                       command=self.update_tampilan_antrian)
        self.btn_refresh.pack(side="right")

        self.label_r_title = ctk.CTkLabel(self.frame_kanan, 
                                          text="RIWAYAT TERAKHIR", 
                                          font=("Arial", 14, "bold"))
        self.label_r_title.grid(row=4, column=0, sticky="w", padx=20, pady=(10, 0))

        self.scroll_riwayat = ctk.CTkScrollableFrame(self.frame_kanan, 
                                                      fg_color="#0d0d0d", 
                                                      height=150)
        self.scroll_riwayat.grid(row=5, column=0, sticky="nsew", padx=20, pady=(5, 20))

        self.update_jam()

    
    #udh masuk logic
    def update_jam(self):
        
        now = datetime.now()
        
        hari_id = {
            "Monday": "Senin", "Tuesday": "Selasa", "Wednesday": "Rabu",
            "Thursday": "Kamis", "Friday": "Jumat", "Saturday": "Sabtu", "Sunday": "Minggu"
        }
        bulan_id = {
            "January": "Januari", "February": "Februari", "March": "Maret",
            "April": "April", "May": "Mei", "June": "Juni",
            "July": "Juli", "August": "Agustus", "September": "September",
            "October": "Oktober", "November": "November", "December": "Desember"
        }
        
        jam = now.strftime("%H:%M:%S")
        self.label_jam.configure(text=jam)
        
        #tnggal indo
        hari_en = now.strftime("%A")
        bulan_en = now.strftime("%B")
        tanggal = now.strftime("%d")
        tahun = now.strftime("%Y")
        
        tgl_format = f"{hari_id[hari_en]}, {tanggal} {bulan_id[bulan_en]} {tahun}"
        self.label_tgl.configure(text=tgl_format)
        
        self.after(1000, self.update_jam) #loop 1s

    def cek_nik_duplikat(self, nik):
        for pasien in self.klinik.antrian_pasien:
            if pasien.get_nik() == nik:
                return True  
        
        for pasien in self.klinik.riwayat_panggilan:
            if pasien.get_nik() == nik:
                return True  
        return False  
    
    def update_stats_display(self):
        total = len(self.klinik.antrian_pasien)
        
        darurat = 0 #ngitung pasien darurat
        for p in self.klinik.antrian_pasien:
            if hasattr(p, 'kategori') and p.kategori == "Darurat":
                darurat += 1
        
        self.lbl_stat_total.configure(text=f"Sisa Antrian: {total}")
        self.lbl_stat_darurat.configure(text=f"Darurat: {darurat}")

    def aksi_daftar(self, event=None):
        nama = self.entry_nama.get().strip()
        nik = self.entry_nik.get().strip()
        keluhan = self.entry_keluhan.get().strip()
        kategori = self.combo_kategori.get()

        if nama == "" or nik == "":
            messagebox.showwarning("Peringatan", "Nama dan NIK wajib diisi!")
            return

        if len(nik) != 16 or not nik.isdigit():
            messagebox.showwarning("Peringatan", 
                                   "NIK harus 16 digit angka!\n(Sesuai standar KTP Indonesia)")
            return

        if self.cek_nik_duplikat(nik):
            messagebox.showerror("Duplikasi Data", 
                                 f"NIK {nik} sudah terdaftar!\n\n"
                                 f"Setiap NIK hanya bisa didaftarkan sekali.\n"
                                 f"Silakan cek kembali data pasien.")
            return

        if keluhan == "":
            keluhan = "Tidak ada keluhan spesifik"

        pasien_baru = Pasien(nama, nik, keluhan, kategori)
        
        self.klinik.tambah_antrian(pasien_baru)
        
        self.update_tampilan_antrian()
        self.update_stats_display()
        self.bersihkan_input()
        
        messagebox.showinfo("Sukses", f"Pasien {nama} berhasil masuk antrian.\nKategori: {kategori}")

    def update_tampilan_antrian(self):
        self.textbox_antrian.configure(state="normal")
        
        self.textbox_antrian.delete("1.0", "end")
        
        #loop pasien di antrian
        nomor = 1
        for pasien in self.klinik.antrian_pasien:
            prefix = "[DARURAT] " if getattr(pasien, 'kategori', 'Umum') == "Darurat" else ""
            
            line = f"{nomor}. {prefix}{pasien.nama} - {pasien.keluhan}\n"
            self.textbox_antrian.insert("end", line)
            nomor += 1
        
        self.textbox_antrian.configure(state="disabled") #biar read only lg

    def update_tampilan_riwayat(self): #update list lg, 5 di riwayat
        for widget in self.scroll_riwayat.winfo_children():
            widget.destroy() #apus yg lama

        recent = list(reversed(self.klinik.riwayat_panggilan))[:5]

        for pasien in recent:
            card = ctk.CTkFrame(self.scroll_riwayat, 
                                fg_color="#2c3e50", 
                                corner_radius=10)
            card.pack(fill="x", pady=3, padx=5)
            
            ctk.CTkLabel(card, 
                         text=f"{pasien.nama}", 
                         font=("Arial", 12, "bold"),
                         anchor="w").pack(padx=10, pady=(8, 2), fill="x")
            
            badge_color = "#e74c3c" if pasien.kategori == "Darurat" else "#3498db"
            ctk.CTkLabel(card, 
                         text=pasien.kategori, 
                         font=("Arial", 10), 
                         text_color=badge_color).pack(padx=10, pady=(0, 8))

    def aksi_panggil(self): #dequeue pasien dr stack
        pasien = self.klinik.panggil_pasien()
        
        if pasien: #update semua ui
            self.update_tampilan_antrian()
            self.update_stats_display()
            self.update_tampilan_riwayat()
            
            messagebox.showinfo("Panggilan Pasien", 
                                f"Memanggil:\n\n"
                                f"Nama: {pasien.nama}\n"
                                f"Keluhan: {pasien.keluhan}\n"
                                f"Kategori: {pasien.kategori}\n\n"
                                f"Silakan masuk ke ruang dokter!")  
        else:
            messagebox.showinfo("Info", "Antrian kosong!\nTidak ada pasien untuk dipanggil.")

    def bersihkan_input(self):
        self.entry_nama.delete(0, "end")
        self.entry_nik.delete(0, "end")
        self.entry_keluhan.delete(0, "end")
        self.combo_kategori.set("Umum")
        self.entry_nama.focus()  

    def resize_bg(self, event):
        if event.widget == self:
            try:
                new_bg_image = ctk.CTkImage(light_image=self.bg_source, 
                                            dark_image=self.bg_source, 
                                            size=(event.width, event.height))
                self.bg_label.configure(image=new_bg_image)
            except:
                pass  

    def on_closing(self):
        try:
            self.destroy()
        except:
            pass

if __name__ == "__main__":
    app = MediQueueApp()
    app.mainloop()