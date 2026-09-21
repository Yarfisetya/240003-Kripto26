def bersihkan_teks(teks):
    # Mengambil huruf saja dan mengubahnya menjadi huruf kapital
    return "".join(huruf for huruf in teks.upper() if huruf.isalpha())


def huruf_ke_angka(huruf):
    return ord(huruf) - ord("A")


def angka_ke_huruf(angka):
    return chr((angka % 26) + ord("A"))


def buat_kunci(kunci, panjang):
    # Mengulang key sampai sepanjang teks
    kunci_extended = ""

    for i in range(panjang):
        kunci_extended += kunci[i % len(kunci)]

    return kunci_extended


def enkripsi(plaintext, kunci):
    plaintext = bersihkan_teks(plaintext)
    kunci = bersihkan_teks(kunci)

    kunci_extended = buat_kunci(kunci, len(plaintext))
    ciphertext = ""

    for huruf_p, huruf_k in zip(plaintext, kunci_extended):
        nilai_p = huruf_ke_angka(huruf_p)
        nilai_k = huruf_ke_angka(huruf_k)

        hasil = (nilai_p + nilai_k) % 26
        ciphertext += angka_ke_huruf(hasil)

    return ciphertext


def dekripsi(ciphertext, kunci):
    ciphertext = bersihkan_teks(ciphertext)
    kunci = bersihkan_teks(kunci)

    kunci_extended = buat_kunci(kunci, len(ciphertext))
    plaintext = ""

    for huruf_c, huruf_k in zip(ciphertext, kunci_extended):
        nilai_c = huruf_ke_angka(huruf_c)
        nilai_k = huruf_ke_angka(huruf_k)

        hasil = (nilai_c - nilai_k) % 26
        plaintext += angka_ke_huruf(hasil)

    return plaintext


def main():
    while True:
        print("\n=== VIGENERE CIPHER ===")
        print("1. Enkripsi")
        print("2. Dekripsi")
        print("3. Exit")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            plaintext = input("Masukkan plaintext : ")
            kunci = input("Masukkan kunci     : ")

            if not bersihkan_teks(kunci):
                print("Kunci harus berisi huruf.")
                continue

            hasil = enkripsi(plaintext, kunci)

            print("Ciphertext         :", hasil)

        elif pilihan == "2":
            ciphertext = input("Masukkan ciphertext: ")
            kunci = input("Masukkan kunci     : ")

            if not bersihkan_teks(kunci):
                print("Kunci harus berisi huruf.")
                continue

            hasil = dekripsi(ciphertext, kunci)

            print("Plaintext          :", hasil)

        elif pilihan == "3":
            print("Program selesai.")
            break

        else:
            print("Pilihan tidak valid. Silakan pilih 1, 2, atau 3.")


main()