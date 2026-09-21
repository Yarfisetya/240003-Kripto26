# Vigenere Cipher dan Autokey Cipher

Huruf diubah menjadi angka: A=0, B=1, ..., Z=25.

- Enkripsi: `C = (P + K) mod 26`
- Dekripsi: `P = (C - K) mod 26`

Keterangan: `P` = plaintext, `K` = kunci, `C` = ciphertext.

## Vigenere Cipher

Kunci **diulang** sampai sepanjang plaintext.

1. Bersihkan plaintext (huruf saja, ubah ke huruf besar).
2. Ulang kunci sampai panjangnya sama dengan plaintext (dipotong jika lebih panjang).
3. Ubah huruf plaintext dan kunci ke angka.
4. Jumlahkan tiap pasangan, lalu `mod 26`.
5. Ubah hasilnya kembali ke huruf.

### Contoh Enkripsi Soal 1

Plaintext `ASPRAKGANTENG`, kunci `YARFISETYANUGRAHA`. Karena karakter kunci < plain text, maka kunci yang dipakai dipotong sepanjang karakter plain menjadi `YARFISETYANUGRAHA`.

| Pt | n(Pt) | K | n(K) | (P + K) mod 26 | C |
|---|---|---|---|---|---|
| A | 0 | Y | 24 | 24 | Y |
| S | 18 | A | 0 | 18 | S |
| P | 15 | R | 17 | 6 | G |
| R | 17 | F | 5 | 22 | W |
| A | 0 | I | 8 | 8 | I |
| K | 10 | S | 18 | 2 | C |
| G | 6 | E | 4 | 10 | K |
| A | 0 | T | 19 | 19 | T |
| N | 13 | Y | 24 | 11 | L |
| T | 19 | A | 0 | 19 | T |
| E | 4 | N | 13 | 17 | R |
| N | 13 | U | 20 | 7 | H |
| G | 6 | G | 6 | 12 | M |

Ciphertext: `YSGWICKTLTRHM`

1. Ulang kunci sepanjang ciphertext.
2. Kurangkan angka ciphertext dengan angka kunci, lalu `mod 26`.
3. Ubah hasilnya kembali ke huruf.

Kunci sudah diketahui sejak awal, jadi seluruh ciphertext bisa didekripsi sekaligus.

## Autokey Cipher

Kunci awal **dilanjutkan dengan plaintext itu sendiri**, tanpa diulang.

1. Bersihkan plaintext.
2. Susun kunci: kunci awal + plaintext, dipotong sepanjang plaintext.
3. Ubah huruf plaintext dan kunci ke angka.
4. Jumlahkan tiap pasangan, lalu `mod 26`.
5. Ubah hasilnya kembali ke huruf.

Dilakukan **bertahap**, karena kunci berikutnya berasal dari plaintext yang baru didekripsi.

1. Dekripsi huruf pertama sebanyak panjang kunci awal memakai kunci awal.
2. Plaintext hasilnya dipakai sebagai kunci untuk huruf ciphertext berikutnya.
3. Ulangi sampai seluruh ciphertext selesai.


## Kasus Kunci Lebih Panjang dari Plaintext

Kunci **dipotong** sepanjang plaintext, dan sisanya tidak dipakai. Pada kasus ini Vigenere dan Autokey menghasilkan ciphertext yang **sama**.

## Output:

<img width="792" height="447" alt="ss1" src="https://github.com/user-attachments/assets/f91971ca-1970-4381-a5c1-483712e3a0c8" />

