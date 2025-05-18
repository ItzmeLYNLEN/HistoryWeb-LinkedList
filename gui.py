import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import ttk

# Node class untuk struktur linked list
class Node:
    def __init__(self, url):
        self.url = url
        self.prev = None
        self.next = None

# Class utama untuk mengelola riwayat browser
class BrowserHistory:
    def __init__(self):
        self.head = None  # Node teratas (terbaru)
        self.current = None  # Node yang sedang aktif

    # Menambahkan URL ke riwayat
    def visit(self, url):
        new_node = Node(url)
        if self.head:
            new_node.next = self.head
            self.head.prev = new_node
        self.head = new_node
        self.current = new_node

    # Kembali ke halaman sebelumnya
    def back(self):
        if self.current and self.current.next:
            self.current = self.current.next
            return True
        return False

    # Maju ke halaman selanjutnya
    def forward(self):
        if self.current and self.current.prev:
            self.current = self.current.prev
            return True
        return False

    # Mengambil halaman saat ini
    def current_page(self):
        return self.current.url if self.current else None

    # Menampilkan semua riwayat
    def show_history(self):
        history = []
        temp = self.head
        while temp:
            history.append((temp.url, temp == self.current))
            temp = temp.next
        return history

    # Menghapus seluruh riwayat
    def clear_history(self):
        self.head = None
        self.current = None

    # Menghapus URL tertentu dari riwayat
    def delete_url(self, target):
        temp = self.head
        while temp:
            if temp.url == target:
                if temp.prev:
                    temp.prev.next = temp.next
                else:
                    self.head = temp.next
                if temp.next:
                    temp.next.prev = temp.prev
                if temp == self.current:
                    self.current = temp.next or temp.prev
                return True
            temp = temp.next
        return False

    # Pindah ke URL tertentu
    def jump_to(self, target):
        temp = self.head
        while temp:
            if temp.url == target:
                self.current = temp
                return True
            temp = temp.next
        return False

# GUI utama aplikasi
class ChromeStyleHistoryApp:
    def __init__(self, root):
        self.history = BrowserHistory()
        self.search_matches = []  # daftar index hasil pencarian
        self.current_match_index = -1

        # Setup tampilan utama
        root.title("Riwayat Penelusuran")
        root.geometry("500x600")
        root.configure(bg="white")

        # Judul aplikasi
        tk.Label(root, text="Gulu Gulu", font=("Inter", 20, "bold"), bg="white").pack(pady=10)

        # Kolom input URL
        search_frame = tk.Frame(root, bg="white")
        search_frame.pack(pady=5)

        self.entry = tk.Entry(search_frame, font=("Inter", 12), width=40)
        self.entry.pack(side=tk.LEFT, padx=(10,5))

        tk.Button(search_frame, text="🔎 Cari", font=("Inter", 10), command=self.visit).pack(side=tk.LEFT)

        # Tombol navigasi mundur dan maju
        nav_frame = tk.Frame(root, bg="white")
        nav_frame.pack(pady=5)
        tk.Button(nav_frame, text="⬅️ Kembali", font=("Inter", 10), command=self.go_back).grid(row=0, column=0, padx=5)
        tk.Button(nav_frame, text="➡️ Maju", font=("Inter", 10), command=self.go_forward).grid(row=0, column=1, padx=5)

        # Label untuk menampilkan halaman aktif
        self.label = tk.Label(root, text="📄 Halaman Saat Ini: -", font=("Inter", 11), bg="white")
        self.label.pack(pady=10)

        tk.Label(root, text="Riwayat Penelusuran", font=("Inter", 15, "bold"), bg="white").pack(pady=10)

        # Daftar riwayat dengan scroll
        list_frame = tk.Frame(root)
        list_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(list_frame, borderwidth=0, bg="white")
        self.scroll_frame = tk.Frame(self.canvas, bg="white")

        self.v_scroll = tk.Scrollbar(list_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.v_scroll.set)

        self.v_scroll.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0,0), window=self.scroll_frame, anchor='nw')
        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Tombol pengaturan
        setting_frame = tk.Frame(root, bg="white")
        setting_frame.pack(pady=5)

        tk.Button(setting_frame, text="🗑️ Hapus Semua", font=("Inter", 10), command=self.clear_history).grid(row=0, column=0, padx=5)
        tk.Button(setting_frame, text="❌ Hapus URL", font=("Inter", 10), command=self.delete_url).grid(row=0, column=1, padx=5)
        tk.Button(setting_frame, text="🚀 Pindah ke URL", font=("Inter", 10), command=self.jump_to_url).grid(row=0, column=2, padx=5)
        tk.Button(setting_frame, text="🔍 Cari URL", font=("Inter", 10), command=self.search_url).grid(row=0, column=3, padx=5)
        tk.Button(setting_frame, text="➡️ Next Match", font=("Inter", 10), command=self.next_match).grid(row=0, column=4, padx=5)

        self.refresh_history_view()

    # Menambahkan kunjungan baru ke riwayat
    def visit(self):
        url = self.entry.get().strip()
        if url:
            self.history.visit(url)
            self.entry.delete(0, tk.END)
            self.update_current_page()
            self.refresh_history_view()

    # Kembali ke URL sebelumnya
    def go_back(self):
        if self.history.back():
            self.update_current_page()
            self.refresh_history_view()
        else:
            messagebox.showinfo("Info", "Tidak ada halaman sebelumnya.")

    # Maju ke URL berikutnya
    def go_forward(self):
        if self.history.forward():
            self.update_current_page()
            self.refresh_history_view()
        else:
            messagebox.showinfo("Info", "Tidak ada halaman selanjutnya.")

    # Update label halaman saat ini
    def update_current_page(self):
        current = self.history.current_page()
        self.label.config(text=f"📄 Halaman Saat Ini: {current if current else '-'}")

    # Menghapus seluruh riwayat
    def clear_history(self):
        self.history.clear_history()
        self.search_matches = []
        self.current_match_index = -1
        self.update_current_page()
        self.refresh_history_view()

    # Menghapus URL spesifik
    def delete_url(self):
        target = simpledialog.askstring("Hapus URL", "Masukkan URL yang ingin dihapus:")
        if target:
            if self.history.delete_url(target):
                self.update_current_page()
                self.refresh_history_view()
                messagebox.showinfo("Sukses", f"URL '{target}' berhasil dihapus.")
            else:
                messagebox.showwarning("Gagal", f"URL '{target}' tidak ditemukan.")

    # Pindah ke URL tertentu
    def jump_to_url(self):
        target = simpledialog.askstring("Pindah ke URL", "Masukkan URL yang ingin dituju:")
        if target:
            if self.history.jump_to(target):
                self.update_current_page()
                self.refresh_history_view()
                messagebox.showinfo("Berhasil", f"Berpindah ke '{target}'.")
            else:
                messagebox.showwarning("Gagal", f"URL '{target}' tidak ditemukan.")

    # Mencari URL di riwayat dan highlight hasilnya
    def search_url(self):
        target = simpledialog.askstring("Cari URL", "Masukkan URL yang ingin dicari:")
        if not target:
            return

        self.search_matches = []
        self.current_match_index = -1

        entries = self.history.show_history()
        for widget in self.scroll_frame.winfo_children():
            widget.config(bg="white")

        for idx, (entry, _) in enumerate(entries):
            if target.lower() in entry.lower():
                self.search_matches.append(idx)

        if self.search_matches:
            self.current_match_index = 0
            self.highlight_matches()
            messagebox.showinfo("Ditemukan", f"Ditemukan {len(self.search_matches)} hasil untuk '{target}'.")
        else:
            messagebox.showwarning("Tidak Ditemukan", f"URL '{target}' tidak ditemukan di riwayat.")

    # Pindah ke highlight selanjutnya
    def next_match(self):
        if self.search_matches:
            self.current_match_index = (self.current_match_index + 1) % len(self.search_matches)
            self.highlight_matches()
        else:
            messagebox.showinfo("Info", "Tidak ada hasil pencarian. Gunakan tombol Cari URL dulu.")

    # Menyorot URL yang ditemukan dari pencarian
    def highlight_matches(self):
        for idx, widget in enumerate(self.scroll_frame.winfo_children()):
            if idx in self.search_matches:
                if idx == self.search_matches[self.current_match_index]:
                    widget.config(bg="#FFEB3B")  # highlight aktif
                else:
                    widget.config(bg="#FFF9C4")  # highlight umum
            else:
                widget.config(bg="white")

    # Menyegarkan daftar tampilan riwayat
    def refresh_history_view(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        history = self.history.show_history()
        for url, is_current in history:
            color = "#0078D7" if is_current else "black"
            label = tk.Label(self.scroll_frame, text=("-> " if is_current else "   ") + url, font=("Segoe UI", 11), fg=color, bg="white", anchor="w", pady=5)
            label.pack(fill=tk.X, padx=10)

        self.highlight_matches()

# Jalankan program
if __name__ == "__main__":
    root = tk.Tk()
    app = ChromeStyleHistoryApp(root)
    root.mainloop()
