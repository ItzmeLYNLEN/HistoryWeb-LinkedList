class Node:
    def __init__(self, url):
        self.url = url
        self.prev = None
        self.next = None

class BrowserHistory:
    def __init__(self):
        self.current = None
        self.head = None

    def visit(self, url):
        new_node = Node(url)
        if self.current:
            self.current.next = new_node
            new_node.prev = self.current
        else:
            self.head = new_node  # halaman pertama
        self.current = new_node
        print(f"📥 Mengunjungi: {url}")

    def back(self):
        if self.current and self.current.prev:
            self.current = self.current.prev
            print(f"⬅️  Kembali ke: {self.current.url}")
        else:
            print("⚠️  Tidak ada halaman sebelumnya.")

    def forward(self):
        if self.current and self.current.next:
            self.current = self.current.next
            print(f"➡️  Maju ke: {self.current.url}")
        else:
            print("⚠️  Tidak ada halaman selanjutnya.")

    def current_page(self):
        if self.current:
            print(f"📄 Halaman saat ini: {self.current.url}")
        else:
            print("🔍 Belum ada halaman yang dikunjungi.")

    def show_history(self):
        print("\n📚 Riwayat Penelusuran:")
        if not self.head:
            print("⚠️  Belum ada riwayat.")
            return
        temp = self.head
        while temp:
            marker = "👉" if temp == self.current else "   "
            print(f"{marker} {temp.url}")
            temp = temp.next

    def clear_history(self):
        self.head = None
        self.current = None
        print("🗑️  Semua riwayat telah dihapus.")

    def delete_url(self, target_url):
        temp = self.head
        found = False
        while temp:
            if temp.url == target_url:
                found = True
                # Update head if deleting first node
                if temp == self.head:
                    self.head = temp.next
                    if self.head:
                        self.head.prev = None
                # Update links if deleting middle or last node
                if temp.prev:
                    temp.prev.next = temp.next
                if temp.next:
                    temp.next.prev = temp.prev
                # Update current if sedang dihapus
                if temp == self.current:
                    self.current = temp.prev or temp.next
                print(f"❌ URL '{target_url}' berhasil dihapus dari riwayat.")
                return
            temp = temp.next
        if not found:
            print(f"⚠️  URL '{target_url}' tidak ditemukan dalam riwayat.")

    def jump_to(self, target_url):
        temp = self.head
        while temp:
            if temp.url == target_url:
                self.current = temp
                print(f"🚀 Berpindah ke: {self.current.url}")
                return
            temp = temp.next
        print(f"❌ URL '{target_url}' tidak ditemukan dalam riwayat.")


def pengaturan(history):
    while True:
        print("\n📂 PENGATURAN")
        print("1. Kembali ke halaman sebelumnya")
        print("2. Maju ke halaman berikutnya")
        print("3. Lihat halaman saat ini")
        print("4. Tampilkan semua riwayat")
        print("5. Kembali ke menu utama")
        print("6. Keluar")
        print("7. Hapus semua riwayat")
        print("8. Hapus URL tertentu")
        print("9. Pindah ke halaman tertentu dalam riwayat")

        pilihan = input("Pilih menu (1-9): ")
        if pilihan == '1':
            history.back()
        elif pilihan == '2':
            history.forward()
        elif pilihan == '3':
            history.current_page()
        elif pilihan == '4':
            history.show_history()
        elif pilihan == '5':
            break
        elif pilihan == '6':
            print("🚪 Keluar dari program. Sampai jumpa!")
            exit()
        elif pilihan == '7':
            history.clear_history()
        elif pilihan == '8':
            url = input("Masukkan URL yang ingin dihapus: ")
            history.delete_url(url)
        elif pilihan == '9':
            url = input("Masukkan URL yang ingin dituju: ")
            history.jump_to(url)
        else:
            print("❌ Pilihan tidak valid. Coba lagi.")


# Menu utama
def menu():
    history = BrowserHistory()
    while True:
        print("\n==============================")
        print("🔎 GOOGLE SEARCH (Sederhana)")
        print("==============================")
        print("1. Kunjungi halaman baru")
        print("2. Pengaturan")
        print("3. Keluar")
        
        pilihan = input("Pilih menu (1-3): ")
        if pilihan == '1':
            url = input("Masukkan kata kunci atau URL: ")
            history.visit(url)
        elif pilihan == '2':
            pengaturan(history)
        elif pilihan == '3':
            print("🚪 Keluar dari program. Terima kasih!")
            break
        else:
            print("❌ Pilihan tidak valid. Coba lagi.")

# Jalankan program
menu()
