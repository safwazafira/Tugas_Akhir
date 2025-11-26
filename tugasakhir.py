
import tkinter as tk
from tkinter import ttk, messagebox
import random
import datetime
import math

TOTAL_MEJA_UMUM = 20
KAPASITAS_MEJA = 6
TOTAL_RUANG_VIP = 5
TOTAL_RUANG_EVENT = 5
STAFF_USERNAME = "izin"
STAFF_PASSWORD = "masukbang"


reservasi_umum = {}
reservasi_vip = {}
reservasi_event = {}

reservation_counter = 0


def next_reservation_id():
    global reservation_counter
    reservation_counter += 1
    return reservation_counter


def parse_date(date_str):
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except Exception:
        return None


def parse_time(time_str):
    try:
        return datetime.datetime.strptime(time_str, "%H:%M").time()
    except Exception:
        return None


def get_taken_tables_umum(date_str):
    taken = set()
    items = reservasi_umum.get(date_str, [])
    for r in items:
        for t in r.get('assigned', []):
            taken.add(int(t))
    return taken


def get_taken_rooms(res_dict, date_str):
    taken = set()
    items = res_dict.get(date_str, [])
    for r in items:
        # assigned contains room numbers (single or list)
        for t in r.get('assigned', []):
            taken.add(int(t))
    return taken


def assign_tables_umum(date_str, num_people):
    needed_tables = math.ceil(num_people / KAPASITAS_MEJA)
    taken = get_taken_tables_umum(date_str)
    all_tables = set(range(1, TOTAL_MEJA_UMUM + 1))
    free = list(all_tables - taken)
    if len(free) < needed_tables:
        return None
    assigned = random.sample(free, needed_tables)
    assigned.sort()
    return [str(x) for x in assigned]


def assign_room_generic(res_dict, date_str, total_rooms):
    taken = get_taken_rooms(res_dict, date_str)
    all_rooms = set(range(1, total_rooms + 1))
    free = list(all_rooms - taken)
    if not free:
        return None
    assigned = [str(random.choice(free))]
    return assigned


class RestoBookApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RestoBook - Sistem Reservasi Meja Restoran")
        self.geometry("880x640")
        self.resizable(False, False)

        self.configure(bg="#0f0f0f")
        style = ttk.Style(self)
        style.theme_use('clam')

        style.configure('TFrame', background='#0f0f0f')
        style.configure('TLabel', background='#0f0f0f', foreground='white', font=('Segoe UI', 10))
        style.configure('Title.TLabel', font=('Segoe UI', 16, 'bold'))
        style.configure('TButton', background='#1f1f1f', foreground='white', font=('Segoe UI', 10))
        style.map('TButton', background=[('active', '#2f2f2f')])
        style.configure('TEntry', fieldbackground='#1f1f1f', foreground='white')
        style.configure('Treeview', background='#1f1f1f', fieldbackground='#1f1f1f', foreground='white')
        style.configure('Treeview.Heading', background='#151515', foreground='white')

        self.container = ttk.Frame(self)
        self.container.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

        header = ttk.Label(self.container, text='Selamat datang di Lembur Kuring - RestoBook', style='Title.TLabel')
        header.pack(pady=8)

        self.main_frame = ttk.Frame(self.container)
        self.main_frame.pack(fill='both', expand=True)

        self.create_main_menu()

    def clear_frame(self, frame):
        for child in frame.winfo_children():
            child.destroy()

    def create_main_menu(self):
        self.clear_frame(self.main_frame)

        left = ttk.Frame(self.main_frame)
        left.place(relx=0.02, rely=0.03, relwidth=0.46, relheight=0.94)

        ttk.Label(left, text='Pilih Peran', font=('Segoe UI', 14, 'bold')).pack(pady=10)

        ttk.Button(left, text='Pelanggan (Reservasi)', command=self.open_customer_form, width=30).pack(pady=8)
        ttk.Button(left, text='Staf (Login)', command=self.open_staff_login, width=30).pack(pady=8)

        right = ttk.Frame(self.main_frame)
        right.place(relx=0.5, rely=0.03, relwidth=0.48, relheight=0.94)

        ttk.Label(right, text='Menu Restoran', font=('Segoe UI', 14, 'bold')).pack(pady=6)

        menu_canvas = tk.Canvas(right, bg='#0f0f0f', highlightthickness=0)
        menu_canvas.pack(fill='both', expand=True)

        menu_items = [
            ('Nasi Goreng Spesial', 'Rp 30.000'),
            ('Mie Goreng Jawa', 'Rp 28.000'),
            ('Sate Ayam Madura (6 tusuk)', 'Rp 35.000'),
            ('Ayam Bakar Taliwang', 'Rp 42.000'),
            ('Ikan Bakar Rica', 'Rp 45.000'),
            ('Sop Buntut', 'Rp 65.000'),
            ('Gado-Gado', 'Rp 25.000'),
            ('Tumis Kangkung', 'Rp 18.000'),
            ('Es Teh Manis', 'Rp 7.000'),
            ('Es Jeruk', 'Rp 10.000'),
            ('Kopi Tubruk', 'Rp 12.000'),
            ('Pisang Goreng', 'Rp 15.000'),
            ('Martabak Manis', 'Rp 40.000'),
            ('Rendang Daging', 'Rp 55.000'),
            ('Nasi Campur (Paket)', 'Rp 33.000'),
            ('Bakso Uruk', 'Rp 20.000'),
            ('Pempek Palembang', 'Rp 22.000'),
            ('Siomay Bandung', 'Rp 19.000'),
            ('Sop Kambing', 'Rp 60.000'),
            ('Es Campur', 'Rp 18.000'),
        ]

        y = 10
        for name, price in menu_items:
            menu_canvas.create_text(10, y, anchor='nw', text=f"{name} - {price}", fill='white', font=('Segoe UI', 10))
            y += 24

    def open_customer_form(self):
        self.clear_frame(self.main_frame)

        frame = ttk.Frame(self.main_frame)
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text='Form Reservasi - Pelanggan', font=('Segoe UI', 14, 'bold')).pack(pady=6)

        form = ttk.Frame(frame)
        form.pack(pady=8)

        # Fields
        ttk.Label(form, text='Nama Lengkap:').grid(row=0, column=0, sticky='w', padx=4, pady=4)
        nama_entry = ttk.Entry(form, width=40)
        nama_entry.grid(row=0, column=1, padx=4, pady=4)

        ttk.Label(form, text='No. HP:').grid(row=1, column=0, sticky='w', padx=4, pady=4)
        hp_entry = ttk.Entry(form, width=40)
        hp_entry.grid(row=1, column=1, padx=4, pady=4)

        ttk.Label(form, text='Tanggal (YYYY-MM-DD):').grid(row=2, column=0, sticky='w', padx=4, pady=4)
        tanggal_entry = ttk.Entry(form, width=40)
        tanggal_entry.grid(row=2, column=1, padx=4, pady=4)

        ttk.Label(form, text='Waktu (HH:MM, maks. 19:00):').grid(row=3, column=0, sticky='w', padx=4, pady=4)
        waktu_entry = ttk.Entry(form, width=40)
        waktu_entry.grid(row=3, column=1, padx=4, pady=4)

        ttk.Label(form, text='Jumlah Orang:').grid(row=4, column=0, sticky='w', padx=4, pady=4)
        orang_spin = tk.Spinbox(form, from_=1, to=200, width=8)
        orang_spin.grid(row=4, column=1, sticky='w', padx=4, pady=4)

        ttk.Label(form, text='Tipe Ruangan:').grid(row=5, column=0, sticky='w', padx=4, pady=4)
        tipe_combo = ttk.Combobox(form, values=['Umum', 'VIP', 'Event'], state='readonly')
        tipe_combo.current(0)
        tipe_combo.grid(row=5, column=1, sticky='w', padx=4, pady=4)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)

        def submit_reservation():
            nama = nama_entry.get().strip()
            hp = hp_entry.get().strip()
            tanggal = tanggal_entry.get().strip()
            waktu = waktu_entry.get().strip()
            try:
                orang = int(orang_spin.get())
            except Exception:
                orang = 0
            tipe = tipe_combo.get()

            if not nama or not hp or not tanggal or not waktu or orang <= 0:
                messagebox.showwarning('Data tidak lengkap', 'Mohon isi semua data dengan benar.')
                return

            d = parse_date(tanggal)
            if not d:
                messagebox.showwarning('Format tanggal salah', 'Gunakan format YYYY-MM-DD, misal: 2025-12-31')
                return

            t = parse_time(waktu)
            if not t:
                messagebox.showwarning('Format waktu salah', 'Gunakan format HH:MM, misal: 19:30')
                return

            date_str = d.isoformat()

            if tipe == 'Umum':
                assigned = assign_tables_umum(date_str, orang)
                if assigned is None:
      
                    messagebox.showinfo('Penuh', f"Maaf, meja umum untuk tanggal {date_str} sudah tidak mencukupi. Silakan pilih tanggal lain.")
                    return
                
                rid = next_reservation_id()
                rec = {
                    'id': rid,
                    'nama': nama,
                    'hp': hp,
                    'tanggal': date_str,
                    'waktu': waktu,
                    'orang': orang,
                    'tipe': 'Umum',
                    'assigned': assigned
                }
                reservasi_umum.setdefault(date_str, []).append(rec)
                messagebox.showinfo('Reservasi berhasil', f"Reservasi berhasil! Kami akan menghubungi anda dalam kurun waktu 24 jam. Nomor meja yang diberikan: {', '.join(assigned)}")
                self.create_main_menu()

            elif tipe == 'VIP':
                assigned = assign_room_generic(reservasi_vip, date_str, TOTAL_RUANG_VIP)
                if assigned is None:
                    messagebox.showinfo('Penuh', f"Maaf, ruangan VIP untuk tanggal {date_str} sudah penuh. Silakan pilih tanggal lain.")
                    return
                rid = next_reservation_id()
                rec = {
                    'id': rid,
                    'nama': nama,
                    'hp': hp,
                    'tanggal': date_str,
                    'waktu': waktu,
                    'orang': orang,
                    'tipe': 'VIP',
                    'assigned': assigned
                }
                reservasi_vip.setdefault(date_str, []).append(rec)
                messagebox.showinfo('Reservasi berhasil', f"Reservasi berhasil! Kami akan menghubungi anda dalam kurun waktu 24 jam. Nomor ruangan VIP: {assigned[0]}")
                self.create_main_menu()

            else:  
                assigned = assign_room_generic(reservasi_event, date_str, TOTAL_RUANG_EVENT)
                if assigned is None:
                    messagebox.showinfo('Penuh', f"Maaf, ruangan Event untuk tanggal {date_str} sudah penuh. Silakan pilih tanggal lain.")
                    return
                rid = next_reservation_id()
                rec = {
                    'id': rid,
                    'nama': nama,
                    'hp': hp,
                    'tanggal': date_str,
                    'waktu': waktu,
                    'orang': orang,
                    'tipe': 'Event',
                    'assigned': assigned
                }
                reservasi_event.setdefault(date_str, []).append(rec)
                messagebox.showinfo('Reservasi berhasil', f"Reservasi berhasil! Kami akan menghubungi anda dalam kurun waktu 24 jam. Nomor ruangan Event: {assigned[0]}")
                self.create_main_menu()

        ttk.Button(btn_frame, text='Submit Reservasi', command=submit_reservation).grid(row=0, column=0, padx=6)
        ttk.Button(btn_frame, text='Kembali', command=self.create_main_menu).grid(row=0, column=1, padx=6)

    def open_staff_login(self):
        self.clear_frame(self.main_frame)

        frame = ttk.Frame(self.main_frame)
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text='Login Staf', font=('Segoe UI', 14, 'bold')).pack(pady=8)

        form = ttk.Frame(frame)
        form.pack(pady=10)

        ttk.Label(form, text='Username:').grid(row=0, column=0, sticky='w', padx=4, pady=4)
        user_entry = ttk.Entry(form, width=30)
        user_entry.grid(row=0, column=1, padx=4, pady=4)

        ttk.Label(form, text='Password:').grid(row=1, column=0, sticky='w', padx=4, pady=4)
        pass_entry = ttk.Entry(form, width=30, show='*')
        pass_entry.grid(row=1, column=1, padx=4, pady=4)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=8)

        def do_login():
            u = user_entry.get().strip()
            p = pass_entry.get().strip()
            if u == STAFF_USERNAME and p == STAFF_PASSWORD:
                self.open_staff_panel()
            else:
                messagebox.showwarning('Login gagal', 'Username atau password salah. Kembali ke halaman utama.')
                self.create_main_menu()

        ttk.Button(btn_frame, text='Login', command=do_login).grid(row=0, column=0, padx=6)
        ttk.Button(btn_frame, text='Batal', command=self.create_main_menu).grid(row=0, column=1, padx=6)

    def open_staff_panel(self):
        self.clear_frame(self.main_frame)

        frame = ttk.Frame(self.main_frame)
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text='Data Reservasi', font=('Segoe UI', 14, 'bold')).pack(pady=6)

        tabs = ttk.Notebook(frame)
        tabs.pack(fill='both', expand=True, padx=6, pady=8)

        tab_umum = ttk.Frame(tabs)
        tab_vip = ttk.Frame(tabs)
        tab_event = ttk.Frame(tabs)

        tabs.add(tab_umum, text='Reservasi Umum')
        tabs.add(tab_vip, text='Reservasi VIP')
        tabs.add(tab_event, text='Reservasi Event')

        cols = ('ID', 'Nama', 'HP', 'Tanggal', 'Waktu', 'Orang', 'Assigned')

        tv_umum = ttk.Treeview(tab_umum, columns=cols, show='headings', height=18)
        for c in cols:
            tv_umum.heading(c, text=c)
            tv_umum.column(c, width=110 if c != 'Nama' else 180, anchor='center')
        tv_umum.pack(fill='both', expand=True, padx=6, pady=6)

        tv_vip = ttk.Treeview(tab_vip, columns=cols, show='headings', height=18)
        for c in cols:
            tv_vip.heading(c, text=c)
            tv_vip.column(c, width=110 if c != 'Nama' else 180, anchor='center')
        tv_vip.pack(fill='both', expand=True, padx=6, pady=6)

        tv_event = ttk.Treeview(tab_event, columns=cols, show='headings', height=18)
        for c in cols:
            tv_event.heading(c, text=c)
            tv_event.column(c, width=110 if c != 'Nama' else 180, anchor='center')
        tv_event.pack(fill='both', expand=True, padx=6, pady=6)

        def refresh_tables():
           
            for i in tv_umum.get_children():
                tv_umum.delete(i)
            for i in tv_vip.get_children():
                tv_vip.delete(i)
            for i in tv_event.get_children():
                tv_event.delete(i)

            for date_str, lst in sorted(reservasi_umum.items()):
                for r in lst:
                    tv_umum.insert('', 'end', values=(r['id'], r['nama'], r['hp'], r['tanggal'], r['waktu'], r['orang'], ','.join(r['assigned'])))

            for date_str, lst in sorted(reservasi_vip.items()):
                for r in lst:
                    tv_vip.insert('', 'end', values=(r['id'], r['nama'], r['hp'], r['tanggal'], r['waktu'], r['orang'], ','.join(r['assigned'])))

            for date_str, lst in sorted(reservasi_event.items()):
                for r in lst:
                    tv_event.insert('', 'end', values=(r['id'], r['nama'], r['hp'], r['tanggal'], r['waktu'], r['orang'], ','.join(r['assigned'])))

        refresh_tables()

        ctrl = ttk.Frame(frame)
        ctrl.pack(pady=6)

        def logout():
            if messagebox.askyesno('Logout', 'Yakin ingin logout?'):
                self.create_main_menu()

        ttk.Button(ctrl, text='Refresh', command=refresh_tables).grid(row=0, column=0, padx=6)
        ttk.Button(ctrl, text='Hapus Reservasi Terpilih (Umum)', command=lambda: delete_selected(tv_umum, 'Umum')).grid(row=0, column=1, padx=6)
        ttk.Button(ctrl, text='Hapus Reservasi Terpilih (VIP)', command=lambda: delete_selected(tv_vip, 'VIP')).grid(row=0, column=2, padx=6)
        ttk.Button(ctrl, text='Hapus Reservasi Terpilih (Event)', command=lambda: delete_selected(tv_event, 'Event')).grid(row=0, column=3, padx=6)
        ttk.Button(ctrl, text='Logout', command=logout).grid(row=0, column=4, padx=6)

        def delete_selected(treeview, tipe):
            sel = treeview.selection()
            if not sel:
                messagebox.showinfo('Tidak ada pilihan', 'Pilih baris terlebih dahulu.')
                return
            if not messagebox.askyesno('Konfirmasi', 'Hapus reservasi terpilih?'):
                return
            for s in sel:
                vals = treeview.item(s, 'values')
                rid = int(vals[0])
                tanggal = vals[3]
            
                if tipe == 'Umum':
                    lst = reservasi_umum.get(tanggal, [])
                    reservasi_umum[tanggal] = [x for x in lst if x['id'] != rid]
                    if not reservasi_umum[tanggal]:
                        del reservasi_umum[tanggal]
                elif tipe == 'VIP':
                    lst = reservasi_vip.get(tanggal, [])
                    reservasi_vip[tanggal] = [x for x in lst if x['id'] != rid]
                    if not reservasi_vip[tanggal]:
                        del reservasi_vip[tanggal]
                else:
                    lst = reservasi_event.get(tanggal, [])
                    reservasi_event[tanggal] = [x for x in lst if x['id'] != rid]
                    if not reservasi_event[tanggal]:
                        del reservasi_event[tanggal]
            refresh_tables()


if __name__ == '__main__':
    app = RestoBookApp()
    app.mainloop()
