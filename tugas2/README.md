# Hill Cipher

Program ini merupakan implementasi sederhana algoritma **Hill Cipher** menggunakan Python. Program mendukung enkripsi, dekripsi, dan pencarian kunci berdasarkan pasangan plaintext-ciphertext.

## Alur Program

1. Program menampilkan menu utama:
	- **Enkripsi**
	- **Dekripsi**
	- **Cari kunci**
	- **Keluar**
2. Teks diubah menjadi angka berdasarkan alfabet `A=0` sampai `Z=25`. Spasi dihapus dan input hanya boleh berisi huruf `A-Z`.
3. Kunci dimasukkan sebagai matriks persegi. Determinan kunci harus relatif prima dengan 26 agar matriks memiliki invers modulo 26.
4. Pada proses enkripsi atau dekripsi:
	- Teks dibagi menjadi beberapa blok sesuai ukuran matriks kunci.
	- Jika panjang teks belum sesuai ukuran blok, karakter `X` ditambahkan sebagai padding.
	- Setiap blok dikalikan dengan matriks kunci modulo 26.
	- Hasil angka diubah kembali menjadi huruf.
5. Pada dekripsi, program menghitung invers matriks kunci terlebih dahulu, kemudian memproses ciphertext menggunakan invers tersebut.
6. Pada menu **Cari kunci**, program menerima pasangan plaintext dan ciphertext, menghitung invers matriks plaintext, lalu mendapatkan kunci dengan rumus:

	`Kunci = Matriks Ciphertext x Invers Matriks Plaintext (mod 26)`

7. Program terus kembali ke menu sampai pengguna memilih **Keluar**.

OUTPUT:
<img width="777" height="462" alt="1" src="https://github.com/user-attachments/assets/6cdbf9d7-114f-4277-ac19-515ee4a83b64" />
<img width="512" height="427" alt="2" src="https://github.com/user-attachments/assets/5ab9b211-68c0-40ed-b25b-bd8e3ae9bdc4" />


- Plaintext `TESTING` dienkripsi menjadi `BOENIDAR` setelah ditambahkan padding `X`.
- Ciphertext `BOENIDAR` berhasil didekripsi kembali menjadi `TESTINGX`.
- Kunci yang ditemukan adalah:

  ```text
  1 2
  2 7
  ```

## Menjalankan Program

Pastikan Python sudah terpasang, lalu jalankan perintah berikut dari folder `pert2`:

```bash
python hillcipher.py
```
