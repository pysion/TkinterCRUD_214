import tkinter as tk
from tkinter import ttk
import sqlite3

def koneksi():
    koneksi = sqlite3.connect("tutorial.db")
    return koneksi

def readdata():
    conn = koneksi()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    conn.close()
    return rows

class LihatData(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Daftar Siswa")
        self.geometry("400x300")

        columns = ("ID", "Name", "Age")
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor=tk.CENTER)
        self.tree.pack(fill=tk.BOTH, expand=True)

        btn_refresh = tk.Button(self, text="Refresh", command=self.bacadata)
        btn_refresh.pack(pady=5)

        self.bacadata()

    def bacadata(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        rows = readdata()
        for row in rows:
            self.tree.insert("", tk.END, values=row)

if __name__ == "__main__":
    app = LihatData()
    app.mainloop()
