import tkinter as tk
from tkinter import simpledialog, messagebox

# Struktur node untuk menyimpan setiap URL
class Node:
    def __init__(self, url):
        self.url = url
        self.prev = None
        self.next = None

# Struktur linked list untuk riwayat browser
class BrowserHistory:
    def __init__(self):
        self.head = None
        self.current = None

    def visit(self, url):
        new_node = Node(url)
        if self.current:
            self.current.next = new_node
            new_node.prev = self.current
        else:
            self.head = new_node
        self.current = new_node

    def back(self):
        if self.current and self.current.prev:
            self.current = self.current.prev
            return True
        return False

    def forward(self):
        if self.current and self.current.next:
            self.current = self.current.next
            return True
        return False

    def current_page(self):
        return self.current.url if self.current else None

    def show_history(self):
        history = []
        temp = self.head
        while temp:
            prefix = "-> " if temp == self.current else "   "
            history.append(f"{prefix}{temp.url}")
            temp = temp.next
        return history

    def clear_history(self):
        self.head = None
        self.current = None

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
                    self.current = temp.prev or temp.next
                return True
            temp = temp.next
        return False

    def jump_to(self, target):
        temp = self.head
        while temp:
            if temp.url == target:
                self.current = temp
                return True
            temp = temp.next
        return False

# GUI
class BrowserApp:
    def __init__(self, root):
        self.history = BrowserHistory()

        root.title("Google Search Sederhana")
        root.geometry("400x450")

        self.entry = tk.Entry(root, width=40)
        self.entry.pack(pady=10)

        tk.Button(root, text="🔎 Kunjungi", command=self.visit).pack()

        self.label = tk.Label(root, text="📄 Halaman Saat Ini: -", wraplength=300)
        self.label.pack(pady=10)

        # Listbox awalnya tidak ditampilkan
        self.history_box = tk.Listbox(root, width=50)
        self.history_box_visible = False  # Flag untuk melacak status tampil/sembunyi

        # Tombol navigasi
        nav_frame = tk.Frame(root)
        nav_frame.pack()

        tk.Button(nav_frame, text="⬅️ Kembali", command=self.go_back).grid(row=0, column=0, padx=5)
        tk.Button(nav_frame, text="➡️ Maju", command=self.go_forward).grid(row=0, column=1, padx=5)
        tk.Button(nav_frame, text="📚 Tampilkan Riwayat", command=self.toggle_history).grid(row=0, column=2, padx=5)

        # Tombol pengaturan
        setting_frame = tk.Frame(root)
        setting_frame.pack(pady=10)

        tk.Button(setting_frame, text="🗑️ Hapus Semua", command=self.clear_history).grid(row=0, column=0, padx=5)
        tk.Button(setting_frame, text="❌ Hapus URL", command=self.delete_url).grid(row=0, column=1, padx=5)
        tk.Button(setting_frame, text="🚀 Pindah ke URL", command=self.jump_to_url).grid(row=0, column=2, padx=5)

    def visit(self):
        url = self.entry.get().strip()
        if url:
            self.history.visit(url)
            self.entry.delete(0, tk.END)
            self.update_current_page()
            self.refresh_history_box()

    def go_back(self):
        if self.history.back():
            self.update_current_page()
            self.refresh_history_box()
        else:
            messagebox.showinfo("Info", "Tidak ada halaman sebelumnya.")

    def go_forward(self):
        if self.history.forward():
            self.update_current_page()
            self.refresh_history_box()
        else:
            messagebox.showinfo("Info", "Tidak ada halaman selanjutnya.")

    def update_current_page(self):
        current = self.history.current_page()
        self.label.config(text=f"📄 Halaman Saat Ini: {current if current else '-'}")

    def toggle_history(self):
        if not self.history_box_visible:
            self.history_box.pack(pady=10)
            self.refresh_history_box()
            self.history_box_visible = True
        else:
            self.history_box.pack_forget()
            self.history_box_visible = False

    def refresh_history_box(self):
        if self.history_box_visible:
            self.history_box.delete(0, tk.END)
            for entry in self.history.show_history():
                self.history_box.insert(tk.END, entry)

    def clear_history(self):
        self.history.clear_history()
        self.update_current_page()
        self.refresh_history_box()

    def delete_url(self):
        target = simpledialog.askstring("Hapus URL", "Masukkan URL yang ingin dihapus:")
        if target:
            if self.history.delete_url(target):
                self.update_current_page()
                self.refresh_history_box()
                messagebox.showinfo("Sukses", f"URL '{target}' berhasil dihapus.")
            else:
                messagebox.showwarning("Gagal", f"URL '{target}' tidak ditemukan.")

    def jump_to_url(self):
        target = simpledialog.askstring("Pindah ke URL", "Masukkan URL yang ingin dituju:")
        if target:
            if self.history.jump_to(target):
                self.update_current_page()
                self.refresh_history_box()
                messagebox.showinfo("Berhasil", f"Berpindah ke '{target}'.")
            else:
                messagebox.showwarning("Gagal", f"URL '{target}' tidak ditemukan.")

# Jalankan aplikasi
if __name__ == "__main__":
    root = tk.Tk()
    app = BrowserApp(root)
    root.mainloop()
