import tkinter as tk
import sqlite3


def centriranje_prozora(win, width, height):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    win.geometry(f"{width}x{height}+{x}+{y}")

def povezivanje_s_bazom():
    connection = sqlite3.connect('moja_baza.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS izbori
                  (id INTEGER PRIMARY KEY,
                   izbor1 TEXT,
                   izbor2 TEXT,
                   izbor3 TEXT,
                   izbor4 TEXT,
                   izbor5 TEXT,
                   izbor6 TEXT,
                   vrijednost NUMERICAL,
                   vrijednost2 NUMERICAL)''')
    return connection, cursor

def prikazi_izbore_iz_baze():
    prozor_baze_podataka = tk.Toplevel()
    prozor_baze_podataka.title("Prikaz Baze Podataka")

    tekstualno_polje = tk.Text(prozor_baze_podataka)
    tekstualno_polje.pack()

    cursor.execute("SELECT * FROM izbori")
    izbori = cursor.fetchall()
    rezultat = "\n".join([str(izbor) for izbor in izbori])
    tekstualno_polje.insert(tk.END, f"Izbori iz baze:\n{rezultat}")

def spremi_sve_izbore_u_bazu():
    izbor1 = padajuci_izbornik_var.get()
    izbor2 = padajuci_izbornik_var2.get()
    izbor3 = padajuci_izbornik_var3.get()
    izbor4 = padajuci_izbornik_var4.get()
    izbor5 = padajuci_izbornik_var5.get()
    izbor6 = padajuci_izbornik_var6.get()

    unos_var_value = unos_var.get()
    unos2_var_value = unos2_var.get()

    if izbor1 == "Odaberi stavku" or izbor2 == "Odaberi stavku" or izbor3 == "Odaberi stavku" or izbor4 == "Odaberi stavku" or izbor5 == "Odaberi stavku" or izbor6 == "Odaberi stavku":
        rezultat.set("Morate odabrati sve izbore prije spremanja!")
        return

    try:
        vrijednost1 = float(unos_var_value)
        vrijednost2 = float(unos2_var_value)

        connection = sqlite3.connect('moja_baza.db')
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO izbori (izbor1, izbor2, izbor3, izbor4, izbor5, izbor6, vrijednost, vrijednost2) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (izbor1, izbor2, izbor3, izbor4, izbor5, izbor6, vrijednost1, vrijednost2))
        connection.commit()

        cursor.close()
        connection.close()

        rezultat.set("Stavke i vrijednost su spremljeni u bazu podataka!")
    except ValueError:
        rezultat.set("Niste unijeli valjani broj!")

def obrisi_podatke_iz_baze():
    try:
        id_to_delete = int(unos_id.get())

        cursor.execute("DELETE FROM izbori WHERE id = ?", (id_to_delete,))
        connection.commit()

        label.config(text=f"Podaci s ID-om {id_to_delete} su izbrisani iz baze podataka!")

    except ValueError:
        label.config(text="Unesite ispravan ID!")

def odaberi_stavku(*args):
    selected_item = padajuci_izbornik_var.get()
    label.config(text=f"Odabrana stavka: {selected_item}")

def prikazi_unos():
    try:
        uneseni_broj = float(unos_var.get())
        rezultat.set(f"Unijeli ste broj: {uneseni_broj:.2f}")
    except ValueError:
        rezultat.set("Niste unijeli valjani broj!")

def prikazi_unos2():
    try:
        uneseni_broj2 = float(unos2_var.get())
        rezultat2.set(f"Unijeli ste broj: {uneseni_broj2:.2f}")
    except ValueError:
        rezultat2.set("Niste unijeli valjani broj!")


prozor = tk.Tk()
prozor.title("Organizacija baze podataka")
prozor.configure(bg='medium aquamarine')

connection = sqlite3.connect('moja_baza.db')
cursor = connection.cursor()

id_to_delete = 1

cursor.execute("DELETE FROM izbori WHERE id = ?", (id_to_delete,))
connection.commit()

gumb_prikazi_bazu = tk.Button(prozor, text="Prikaži Bazu", command=prikazi_izbore_iz_baze, width=20, height=2)
gumb_prikazi_bazu.grid(row=0, column=7, padx=10, pady=10)
gumb_prikazi_bazu.configure(bg='light gray')

gumb_spremi_sve_izbore = tk.Button(prozor, text="Spremi Sve Izbore", command=spremi_sve_izbore_u_bazu, width=20, height=2)
gumb_spremi_sve_izbore.grid(row=1, column=7, padx=10, pady=10)
gumb_spremi_sve_izbore.configure(bg='light gray')

gumb_obrisi_podatke = tk.Button(prozor, text="Obriši Podatke", command=obrisi_podatke_iz_baze, width=20, height=2)
gumb_obrisi_podatke.grid(row=2, column=7, padx=10, pady=10)
gumb_obrisi_podatke.configure(bg='light gray')

label = tk.Label(prozor, text="")
label.grid(row=4, column=7, padx=10, pady=10)
label.configure(bg='medium aquamarine')

unos_id = tk.Entry(prozor)
unos_id.grid(row=3, column=7, padx=10, pady=10)

unos_var = tk.StringVar()
unos = tk.Entry(prozor, textvariable=unos_var)
unos.grid(row=0, column=4, padx=10, pady=10)

unos2_var = tk.StringVar()
unos2 = tk.Entry(prozor, textvariable=unos2_var)
unos2.grid(row=1, column=4, padx=10, pady=10)

label_rezultat = tk.Label(prozor, text="Odabir promjera alata:")
label_rezultat.grid(row=0, column=3, padx=10, pady=10)
label_rezultat.configure(bg='medium aquamarine')

gumb_potvrdi_unos = tk.Button(prozor, text="Potvrdi unos", command=prikazi_unos)
gumb_potvrdi_unos.grid(row=0, column=6, padx=10, pady=10)
gumb_potvrdi_unos.configure(bg='light gray')

rezultat = tk.StringVar()
rezultat_label = tk.Label(prozor, textvariable=rezultat)
rezultat_label.grid(row=2, column=4, padx=10, pady=10)
rezultat_label.configure(bg='medium aquamarine')

label_rezultat2 = tk.Label(prozor, text="Odabir dužine alata:")
label_rezultat2.grid(row=1, column=3, padx=10, pady=10)
label_rezultat2.configure(bg='medium aquamarine')

gumb_potvrdi_unos2 = tk.Button(prozor, text="Potvrdi unos", command=prikazi_unos2)
gumb_potvrdi_unos2.grid(row=1, column=6, padx=10, pady=10)
gumb_potvrdi_unos2.configure(bg='light gray')

rezultat2 = tk.StringVar()
rezultat2_label = tk.Label(prozor, textvariable=rezultat2)
rezultat2_label.grid(row=3, column=4, padx=10, pady=10)
rezultat2_label.configure(bg='medium aquamarine')

label_izbornik1 = tk.Label(prozor, text="Odabir vrste alata:")
label_izbornik1.grid(row=0, column=0, padx=10, pady=10)
label_izbornik1.configure(bg='medium aquamarine')

padajuci_izbornik_var = tk.StringVar()
padajuci_izbornik_var.set("Odaberi stavku")
padajuci_izbornik = tk.OptionMenu(prozor, padajuci_izbornik_var, "Glodalo", "Svrdlo", "Glodača glava", "Svrdlo s pločicama", "Pilot svrdlo","Trkač")
padajuci_izbornik.grid(row=0, column=1, padx=10, pady=10)
padajuci_izbornik.configure(bg='light gray')

label_izbornik2 = tk.Label(prozor, text="Odabir vrste prihvata:")
label_izbornik2.grid(row=3, column=0, padx=10, pady=10)
label_izbornik2.configure(bg='medium aquamarine')

padajuci_izbornik_var2 = tk.StringVar()
padajuci_izbornik_var2.set("Odaberi stavku")
padajuci_izbornik2 = tk.OptionMenu(prozor, padajuci_izbornik_var2, "SK40", "SK50", "HSK50", "HSK63")
padajuci_izbornik2.grid(row=3, column=1, padx=10, pady=10)
padajuci_izbornik2.configure(bg='light gray')

label_izbornik3 = tk.Label(prozor, text="Odabir proizvođača alata:")
label_izbornik3.grid(row=2, column=0, padx=10, pady=10)
label_izbornik3.configure(bg='medium aquamarine')

padajuci_izbornik_var3 = tk.StringVar()
padajuci_izbornik_var3.set("Odaberi stavku")
padajuci_izbornik3 = tk.OptionMenu(prozor, padajuci_izbornik_var3, "Walter", "Seco", "Guehring", "Emuge", "SAB d.o.o","Aura","Sandivk")
padajuci_izbornik3.grid(row=2, column=1, padx=10, pady=10)
padajuci_izbornik3.configure(bg='light gray')

label_izbornik4 = tk.Label(prozor, text="Odabir načina obrade alata:")
label_izbornik4.grid(row=1, column=0, padx=10, pady=10)
label_izbornik4.configure(bg='medium aquamarine')

padajuci_izbornik_var4 = tk.StringVar()
padajuci_izbornik_var4.set("Odaberi stavku")
padajuci_izbornik4 = tk.OptionMenu(prozor, padajuci_izbornik_var4, "Gruba", "Polufina", "Fina")
padajuci_izbornik4.grid(row=1, column=1, padx=10, pady=10)
padajuci_izbornik4.configure(bg='light gray')

label_izbornik5 = tk.Label(prozor, text="Odabir radnog mjesta alata:")
label_izbornik5.grid(row=4, column=0, padx=10, pady=10)
label_izbornik5.configure(bg='medium aquamarine')

padajuci_izbornik_var5 = tk.StringVar()
padajuci_izbornik_var5.set("Odaberi stavku")
padajuci_izbornik5 = tk.OptionMenu(prozor, padajuci_izbornik_var5, "HAAS VM2", "HAAS VM3", "HAAS VF8", "Mikron 800P", "Mikron 1350U", "Mikron 1850U", "DMG HSC55", "CHETO")
padajuci_izbornik5.grid(row=4, column=1, padx=10, pady=10)
padajuci_izbornik5.configure(bg='light gray')

label_izbornik6 = tk.Label(prozor, text="Odabir radnika:")
label_izbornik6.grid(row=5, column=0, padx=10, pady=10)
label_izbornik6.configure(bg='medium aquamarine')

padajuci_izbornik_var6 = tk.StringVar()
padajuci_izbornik_var6.set("Odaberi stavku")
padajuci_izbornik6 = tk.OptionMenu(prozor, padajuci_izbornik_var6, "Antonio Kvas", "Ivan Perić", "Karlo Vidić", "Renato Rogar", "Božidar Debeljak", "Nikola Bogeljić", "Robert Višnjevac", "Iva Jurić", "Bruno Došen")
padajuci_izbornik6.grid(row=5, column=1, padx=10, pady=10)
padajuci_izbornik6.configure(bg='light gray')

padajuci_izbornik_var.trace("w", odaberi_stavku)
padajuci_izbornik_var2.trace("w", odaberi_stavku)
padajuci_izbornik_var3.trace("w", odaberi_stavku)
padajuci_izbornik_var4.trace("w", odaberi_stavku)
padajuci_izbornik_var5.trace("w", odaberi_stavku)
padajuci_izbornik_var6.trace("w", odaberi_stavku)

width = 1200
height = 400
centriranje_prozora(prozor, width, height)

prozor.mainloop()

cursor.close()
connection.close()


