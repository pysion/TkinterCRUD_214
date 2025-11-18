import sqlite3
import tkinter as tk
import tkinter.messagebox as msg
from tkinter import ttk


def koneksi():
    con = sqlite3.connect("tutorial.db")
    return con

def create_table():
    con = koneksi()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER
        )
    """)
    con.commit()
    con.close()

def insertsiswa(name: str, age: int):
    con = koneksi()
    cur = con.cursor()
    cur.execute("INSERT INTO students (name, age) VALUES (?, ?)", (name, age))
    con.commit()
    rowid = cur.lastrowid
    con.close()
    return rowid

def readsiswa():
    con = koneksi()
    cur = con.cursor()
    cur.execute("SELECT id, name, age FROM students ORDER BY id")
    rows = cur.fetchall()
    con.close()
    return rows


create_table()

class Mahasiswa(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Insert dan Read Data Mahasiswa")
        self.geometry("600x420")
        self.configure(bg="#f0f2f5")

        frm = tk.Frame(self, bg="#ffffff", padx=12, pady=12)
        frm.pack(padx=16, pady=12, fill="x")

        tk.Label(frm, text="Nama:", bg="#ffffff").grid(row=0, column=0, sticky="w")
        self.ent_name = tk.Entry(frm, width=30)
        self.ent_name.grid(row=0, column=1, sticky="w", padx=6, pady=6)

        tk.Label(frm, text="Umur:", bg="#ffffff").grid(row=1, column=0, sticky="w")
        self.ent_age = tk.Entry(frm, width=30)
        self.ent_age.grid(row=1, column=1, sticky="w", padx=6, pady=6)

        btn_frame = tk.Frame(frm, bg="#ffffff")
        btn_frame.grid(row=2, column=0, columnspan=2, pady=(6,0))

        self.btn_add = tk.Button(btn_frame, text="Tambah", width=10, command=self.insertdata)
        self.btn_add.pack(side="left", padx=6)
        self.btn_refresh = tk.Button(btn_frame, text="Refresh", width=10, command=self.read_data)
        self.btn_refresh.pack(side="left", padx=6)

        cols = ("id", "name", "age")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=12)
        self.tree.heading("id", text="ID")
        self.tree.column("id", width=50, anchor="center")
        self.tree.heading("name", text="Nama")
        self.tree.column("name", width=350)
        self.tree.heading("age", text="Umur")
        self.tree.column("age", width=80, anchor="center")
        self.tree.pack(padx=16, pady=(0,12), fill="both", expand=True)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.read_data()

    def clear_inputs(self):
        self.ent_name.delete(0, tk.END)
        self.ent_age.delete(0, tk.END)

    def validate_inputs(self):
        name = self.ent_name.get().strip()
        age_str = self.ent_age.get().strip()
        if not name or not age_str:
            msg.showwarning("Peringatan", "Nama dan umur tidak boleh kosong.")
            return None
        try:
            age = int(age_str)
            if age < 0:
                raise ValueError
        except ValueError:
            msg.showerror("Salah", "Umur harus bilangan bulat >= 0.")
            return None
        return name, age

    def insertdata(self):
        val = self.validate_inputs()
        if not val:
            return
        name, age = val
        try:
            new_id = insertsiswa(name, age)
            msg.showinfo("Sukses", f"Data disimpan (id={new_id}).")
            self.read_data()
            self.clear_inputs()
        except Exception as e:
            msg.showerror("DB Error", str(e))

    def on_tree_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        item = self.tree.item(sel[0])
        _, name, age = item["values"]
        self.ent_name.insert(0, name)
        self.ent_age.insert(0, str(age))

    def read_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            rows = readsiswa()
            for r in rows:
                self.tree.insert("", tk.END, values=r)
        except Exception as e:
            msg.showerror("DB Error", str(e))

if __name__ == "__main__":
    app = Mahasiswa()
    app.mainloop()
