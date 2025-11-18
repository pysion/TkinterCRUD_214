import sqlite3
import tkinter as tk
import tkinter.messagebox as msg
from tkinter import ttk


def koneksi():
    con = sqlite3.connect("nilai_siswa.db")
    return con

def create_table():
    con = koneksi()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            nim TEXT PRIMARY KEY,
            nama_mahasiswa TEXT NOT NULL,
            biologi INTEGER NOT NULL,
            fisika INTEGER NOT NULL,
            inggris INTEGER NOT NULL,
            prediksi_fakultas TEXT NOT NULL
        )
    """)
    con.commit()
    con.close()

def insert_nilai(nim: str, nama: str, biologi: int, fisika: int, inggris: int, prediksi: str):
    con = koneksi()
    cur = con.cursor()
    cur.execute("""
        INSERT INTO nilai_siswa (nim, nama_mahasiswa, biologi, fisika, inggris, prediksi_fakultas) 
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nim, nama, biologi, fisika, inggris, prediksi))
    con.commit()
    con.close()
    return nim

def read_nilai():
    con = koneksi()
    cur = con.cursor()
    cur.execute("""
        SELECT nim, nama_mahasiswa, biologi, fisika, inggris, prediksi_fakultas 
        FROM nilai_siswa ORDER BY nim
    """)
    rows = cur.fetchall()
    con.close()
    return rows


create_table()

class AplikasiPrediksi(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Prediksi Fakultas Berdasarkan Nilai")
        self.geometry("800x520")
        self.configure(bg="#f0f2f5")

        # Frame Input
        frm = tk.Frame(self, bg="#ffffff", padx=15, pady=15)
        frm.pack(padx=16, pady=12, fill="x")

        # NIM
        tk.Label(frm, text="NIM:", bg="#ffffff", font=("Arial", 10)).grid(
            row=0, column=0, sticky="w", pady=5
        )
        self.ent_nim = tk.Entry(frm, width=35, font=("Arial", 10))
        self.ent_nim.grid(row=0, column=1, sticky="w", padx=10, pady=5)

        # Nama Mahasiswa
        tk.Label(frm, text="Nama Mahasiswa:", bg="#ffffff", font=("Arial", 10)).grid(
            row=1, column=0, sticky="w", pady=5
        )
        self.ent_nama = tk.Entry(frm, width=35, font=("Arial", 10))
        self.ent_nama.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        # Nilai Biologi
        tk.Label(frm, text="Nilai Biologi:", bg="#ffffff", font=("Arial", 10)).grid(
            row=2, column=0, sticky="w", pady=5
        )
        self.ent_biologi = tk.Entry(frm, width=35, font=("Arial", 10))
        self.ent_biologi.grid(row=2, column=1, sticky="w", padx=10, pady=5)

        # Nilai Fisika
        tk.Label(frm, text="Nilai Fisika:", bg="#ffffff", font=("Arial", 10)).grid(
            row=3, column=0, sticky="w", pady=5
        )
        self.ent_fisika = tk.Entry(frm, width=35, font=("Arial", 10))
        self.ent_fisika.grid(row=3, column=1, sticky="w", padx=10, pady=5)

        # Nilai Inggris
        tk.Label(frm, text="Nilai Inggris:", bg="#ffffff", font=("Arial", 10)).grid(
            row=4, column=0, sticky="w", pady=5
        )
        self.ent_inggris = tk.Entry(frm, width=35, font=("Arial", 10))
        self.ent_inggris.grid(row=4, column=1, sticky="w", padx=10, pady=5)

        # Prediksi Fakultas (Read-only)
        tk.Label(frm, text="Prediksi Fakultas:", bg="#ffffff", font=("Arial", 10, "bold")).grid(
            row=5, column=0, sticky="w", pady=5
        )
        self.lbl_prediksi = tk.Label(
            frm, text="-", bg="#ffffff", font=("Arial", 10, "bold"), 
            fg="#0066cc", anchor="w", width=33
        )
        self.lbl_prediksi.grid(row=5, column=1, sticky="w", padx=10, pady=5)

        # Buttons
        btn_frame = tk.Frame(frm, bg="#ffffff")
        btn_frame.grid(row=6, column=0, columnspan=2, pady=(10, 0))

        self.btn_submit = tk.Button(
            btn_frame, text="Submit Nilai", width=12, 
            command=self.submit_nilai, bg="#4CAF50", fg="white", font=("Arial", 9, "bold")
        )
        self.btn_submit.pack(side="left", padx=5)

        self.btn_refresh = tk.Button(
            btn_frame, text="Refresh", width=12, 
            command=self.read_data, bg="#2196F3", fg="white", font=("Arial", 9, "bold")
        )
        self.btn_refresh.pack(side="left", padx=5)

        self.btn_clear = tk.Button(
            btn_frame, text="Clear", width=12, 
            command=self.clear_inputs, bg="#FF9800", fg="white", font=("Arial", 9, "bold")
        )
        self.btn_clear.pack(side="left", padx=5)

        # Treeview
        cols = ("nim", "nama", "biologi", "fisika", "inggris", "prediksi")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=12)
        
        self.tree.heading("nim", text="NIM")
        self.tree.column("nim", width=100, anchor="center")
        
        self.tree.heading("nama", text="Nama Mahasiswa")
        self.tree.column("nama", width=200)
        
        self.tree.heading("biologi", text="Biologi")
        self.tree.column("biologi", width=80, anchor="center")
        
        self.tree.heading("fisika", text="Fisika")
        self.tree.column("fisika", width=80, anchor="center")
        
        self.tree.heading("inggris", text="Inggris")
        self.tree.column("inggris", width=80, anchor="center")
        
        self.tree.heading("prediksi", text="Prediksi Fakultas")
        self.tree.column("prediksi", width=200, anchor="center")
        
        self.tree.pack(padx=16, pady=(0, 12), fill="both", expand=True)

        # Bind nilai input untuk prediksi otomatis
        self.ent_biologi.bind("<KeyRelease>", self.auto_prediksi)
        self.ent_fisika.bind("<KeyRelease>", self.auto_prediksi)
        self.ent_inggris.bind("<KeyRelease>", self.auto_prediksi)

        self.read_data()

    def clear_inputs(self):
        self.ent_nim.delete(0, tk.END)
        self.ent_nama.delete(0, tk.END)
        self.ent_biologi.delete(0, tk.END)
        self.ent_fisika.delete(0, tk.END)
        self.ent_inggris.delete(0, tk.END)
        self.lbl_prediksi.config(text="-")

    def prediksi_fakultas(self, biologi: int, fisika: int, inggris: int) -> str:
        """
        Logika prediksi:
        - Jika Biologi paling tinggi -> Kedokteran
        - Jika Fisika paling tinggi -> Teknik
        - Jika Inggris paling tinggi -> Bahasa
        """
        nilai_max = max(biologi, fisika, inggris)
        
        if biologi == nilai_max:
            return "Kedokteran"
        elif fisika == nilai_max:
            return "Teknik"
        else:
            return "Bahasa"

    def auto_prediksi(self, event=None):
        """Update prediksi otomatis saat nilai diketik"""
        try:
            biologi = int(self.ent_biologi.get().strip())
            fisika = int(self.ent_fisika.get().strip())
            inggris = int(self.ent_inggris.get().strip())
            
            prediksi = self.prediksi_fakultas(biologi, fisika, inggris)
            self.lbl_prediksi.config(text=prediksi)
        except ValueError:
            self.lbl_prediksi.config(text="-")

    def validate_inputs(self):
        nim = self.ent_nim.get().strip()
        nama = self.ent_nama.get().strip()
        bio_str = self.ent_biologi.get().strip()
        fis_str = self.ent_fisika.get().strip()
        ing_str = self.ent_inggris.get().strip()
        
        if not nim:
            msg.showwarning("Peringatan", "NIM tidak boleh kosong.")
            return None
        
        if not nama:
            msg.showwarning("Peringatan", "Nama mahasiswa tidak boleh kosong.")
            return None
        
        if not bio_str or not fis_str or not ing_str:
            msg.showwarning("Peringatan", "Semua nilai harus diisi.")
            return None
        
        try:
            biologi = int(bio_str)
            fisika = int(fis_str)
            inggris = int(ing_str)
            
            if biologi < 0 or biologi > 100:
                raise ValueError("Nilai Biologi harus 0-100")
            if fisika < 0 or fisika > 100:
                raise ValueError("Nilai Fisika harus 0-100")
            if inggris < 0 or inggris > 100:
                raise ValueError("Nilai Inggris harus 0-100")
                
        except ValueError as e:
            msg.showerror("Salah", f"Nilai harus bilangan bulat 0-100.\n{str(e)}")
            return None
        
        return nim, nama, biologi, fisika, inggris

    def submit_nilai(self):
        val = self.validate_inputs()
        if not val:
            return
        
        nim, nama, biologi, fisika, inggris = val
        prediksi = self.prediksi_fakultas(biologi, fisika, inggris)
        
        try:
            insert_nilai(nim, nama, biologi, fisika, inggris, prediksi)
            msg.showinfo("Sukses", f"Data berhasil disimpan!\nNIM: {nim}\nPrediksi: {prediksi}")
            self.read_data()
            self.clear_inputs()
        except Exception as e:
            msg.showerror("DB Error", str(e))

    def read_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            rows = read_nilai()
            for r in rows:
                self.tree.insert("", tk.END, values=r)
        except Exception as e:
            msg.showerror("DB Error", str(e))


if __name__ == "__main__":
    app = AplikasiPrediksi()
    app.mainloop()