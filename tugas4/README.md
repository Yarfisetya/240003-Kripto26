# Tugas 4 Kriptografi - Steganografi LSB

## Deskripsi

Program ini merupakan implementasi steganografi menggunakan metode **Least Significant Bit (LSB)**. Program digunakan untuk menyembunyikan pesan teks ke dalam gambar dan mengambil kembali pesan tersebut dari gambar hasil steganografi.

Metode yang digunakan adalah **LSB Sequential**, yaitu bit pesan disisipkan secara berurutan pada bit paling rendah (LSB) dari channel RGB pada gambar.

## Teknologi yang Digunakan

- Python
- Pillow
- Metode Steganografi LSB Sequential
- Format gambar PNG

## Struktur Program

```text
240003-Kripto26/
├── main.py
├── lsb.py
└── images/
    ├── cover.png
    └── stego.png
```

### Keterangan

- `main.py` digunakan untuk menjalankan program dan mengatur menu.
- `lsb.py` berisi fungsi-fungsi utama untuk proses steganografi LSB.
- `cover.png` merupakan gambar asli yang digunakan sebagai media penyisipan pesan.
- `stego.png` merupakan gambar hasil penyisipan pesan.

---

# Penjelasan Fungsi

## `main.py`

### 1. `show_capacity()`

```python
def show_capacity():
    image_path = input("Masukkan path gambar: ")
    try:
        image = Image.open(image_path)
        capacity = get_capacity(image)
        max_bytes = (capacity - 32) // 8

        print("\nInformasi Gambar")
        print("------------------------")
        print(f"Ukuran gambar : {image.width} x {image.height}")
        print(f"Kapasitas bit : {capacity} bit")
        print(f"Kapasitas pesan : {max_bytes} byte")
    except Exception as e:
        print(f"Error: {e}")
```

**Penjelasan:**  
Digunakan untuk mengecek kapasitas gambar yang dapat digunakan untuk menyisipkan pesan. Fungsi menampilkan ukuran gambar, kapasitas bit, dan kapasitas maksimum pesan dalam byte.

---

### 2. `encode_menu()`

```python
def encode_menu():
    image_path = input("Masukkan gambar cover : ")
    output_path = input("Masukkan nama output : ")
    message = input("Masukkan pesan rahasia : ")

    try:
        encode(image_path, message, output_path)
        print("\nPesan berhasil disembunyikan!")
        print(f"Stego image : {output_path}")
    except Exception as e:
        print(f"\nGagal melakukan encode: {e}")
```

**Penjelasan:**  
Digunakan untuk menerima input gambar cover, nama file output, dan pesan rahasia. Setelah itu fungsi memanggil `encode()` untuk menyisipkan pesan ke dalam gambar.

---

### 3. `decode_menu()`

```python
def decode_menu():
    image_path = input("Masukkan gambar stego : ")

    try:
        message = decode(image_path)

        print("\nPesan tersembunyi:")
        print("------------------------")
        print(message)
    except Exception as e:
        print(f"\nGagal melakukan decode: {e}")
```

**Penjelasan:**  
Digunakan untuk menerima path gambar stego dan menampilkan pesan yang tersembunyi di dalam gambar menggunakan fungsi `decode()`.

---

### 4. `main()`

```python
def main():
    while True:
        print("\n================================")
        print("     STEGANOGRAPHY - LSB")
        print("================================")
        print("1. Encode pesan")
        print("2. Decode pesan")
        print("3. Cek kapasitas gambar")
        print("4. Keluar")
        print("================================")

        choice = input("Pilih menu: ")

        if choice == "1":
            encode_menu()
        elif choice == "2":
            decode_menu()
        elif choice == "3":
            show_capacity()
        elif choice == "4":
            print("Program selesai.")
            break
        else:
            print("Pilihan tidak valid.")
```

**Penjelasan:**  
Merupakan fungsi utama yang mengatur menu program. Pengguna dapat memilih proses encode, decode, pengecekan kapasitas gambar, atau keluar dari program.

---

# `lsb.py`

### 5. `text_to_bytes()`

```python
def text_to_bytes(text):
    return text.encode("utf-8")
```

**Penjelasan:**  
Mengubah pesan teks menjadi byte menggunakan encoding UTF-8 sebelum diproses menjadi bit.

---

### 6. `bytes_to_bits()`

```python
def bytes_to_bits(data):
    bits = []

    for byte in data:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)

    return bits
```

**Penjelasan:**  
Mengubah setiap byte dari pesan menjadi kumpulan bit `0` dan `1` yang digunakan dalam proses penyisipan pesan.

---

### 7. `bits_to_bytes()`

```python
def bits_to_bytes(bits):
    data = bytearray()

    for i in range(0, len(bits), 8):
        byte = 0

        for bit in bits[i:i + 8]:
            byte = (byte << 1) | bit

        data.append(byte)

    return bytes(data)
```

**Penjelasan:**  
Mengubah kumpulan bit hasil ekstraksi menjadi byte kembali sehingga dapat diterjemahkan menjadi pesan teks.

---

### 8. `int_to_bits()`

```python
def int_to_bits(number):
    bits = []

    for i in range(31, -1, -1):
        bits.append((number >> i) & 1)

    return bits
```

**Penjelasan:**  
Mengubah nilai panjang pesan menjadi 32 bit. Nilai tersebut digunakan sebagai header untuk menyimpan informasi panjang pesan.

---

### 9. `bits_to_int()`

```python
def bits_to_int(bits):
    number = 0

    for bit in bits:
        number = (number << 1) | bit

    return number
```

**Penjelasan:**  
Mengubah 32 bit header yang telah diekstraksi dari gambar menjadi nilai panjang pesan.

---

### 10. `get_capacity()`

```python
def get_capacity(image):
    width, height = image.size
    return width * height * 3
```

**Penjelasan:**  
Menghitung kapasitas bit yang tersedia pada gambar berdasarkan ukuran gambar dan tiga channel RGB.

---

### 11. `encode()`

```python
def encode(image_path, message, output_path):
    image = Image.open(image_path).convert("RGBA")
    message_bytes = text_to_bytes(message)
    length_bits = int_to_bits(len(message_bytes))
    message_bits = bytes_to_bits(message_bytes)
    data_bits = length_bits + message_bits

    capacity = get_capacity(image)

    if len(data_bits) > capacity:
        max_bytes = (capacity - HEADER_SIZE) // 8
        raise ValueError(
            f"Pesan terlalu besar!\n"
            f"Maksimal pesan: {max_bytes} byte"
        )

    pixels = image.load()
    bit_index = 0

    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = pixels[x, y]
            channels = [r, g, b]

            for i in range(3):
                if bit_index >= len(data_bits):
                    break

                channels[i] = (
                    channels[i] & 0b11111110
                ) | data_bits[bit_index]

                bit_index += 1

            pixels[x, y] = (
                channels[0],
                channels[1],
                channels[2],
                a
            )

            if bit_index >= len(data_bits):
                break

        if bit_index >= len(data_bits):
            break

    image.save(output_path, "PNG")
```

**Penjelasan:**  
Melakukan proses penyisipan pesan menggunakan metode **LSB Sequential**. Pesan diubah menjadi bit, kemudian setiap bit disisipkan secara berurutan pada LSB channel RGB gambar. Hasilnya disimpan sebagai stego-image dalam format PNG.

---

### 12. `decode()`

```python
def decode(image_path):
    image = Image.open(image_path).convert("RGBA")
    pixels = image.load()

    length_bits = []
    bit_count = 0

    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = pixels[x, y]
            channels = [r, g, b]

            for channel in channels:
                if bit_count >= HEADER_SIZE:
                    break

                length_bits.append(channel & 1)
                bit_count += 1

            if bit_count >= HEADER_SIZE:
                break

        if bit_count >= HEADER_SIZE:
            break

    message_length = bits_to_int(length_bits)
    message_bit_count = message_length * 8

    message_bits = []
    bit_count = 0

    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = pixels[x, y]
            channels = [r, g, b]

            for channel in channels:
                if bit_count < HEADER_SIZE:
                    bit_count += 1
                    continue

                if len(message_bits) >= message_bit_count:
                    break

                message_bits.append(channel & 1)

            if len(message_bits) >= message_bit_count:
                break

        if len(message_bits) >= message_bit_count:
            break

    message_bytes = bits_to_bytes(message_bits)

    return message_bytes.decode("utf-8")
```

**Penjelasan:**  
Melakukan proses ekstraksi pesan dari stego-image. Program membaca LSB channel RGB, mengambil 32 bit pertama sebagai informasi panjang pesan, kemudian mengambil bit pesan sesuai panjang tersebut dan mengubahnya kembali menjadi teks.

---

# Alur Kerja Program

```text
                    main()
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
 encode_menu()  decode_menu()  show_capacity()
        │             │             │
        ▼             ▼             ▼
    encode()      decode()   get_capacity()
        │             │
        ▼             ▼
   Pesan → Bit    LSB → Bit
        │             │
        ▼             ▼
  Stego Image     Byte → Teks
```

## Proses Encode

```text
Pesan Teks
    ↓
UTF-8 / Byte
    ↓
Bit
    ↓
Header 32-bit
    ↓
Penyisipan ke LSB RGB
    ↓
Stego Image (.png)
```

## Proses Decode

```text
Stego Image (.png)
    ↓
Membaca LSB RGB
    ↓
Membaca Header 32-bit
    ↓
Menentukan Panjang Pesan
    ↓
Mengambil Bit Pesan
    ↓
Bit → Byte
    ↓
Byte → Teks
    ↓
Pesan Asli
```

# Cara Menjalankan Program

## 1. Install Pillow

```bash
pip install pillow
```

## 2. Jalankan Program

```bash
python main.py
```

## 3. Menu Program

```text
================================
     STEGANOGRAPHY - LSB
================================
1. Encode pesan
2. Decode pesan
3. Cek kapasitas gambar
4. Keluar
================================
Pilih menu:
```

## 4. Encode Pesan

Pilih menu:

```text
1
```

Kemudian masukkan path gambar cover, nama file output, dan pesan rahasia.

Contoh:

```text
Masukkan gambar cover : images/cover.png
Masukkan nama output : images/stego.png
Masukkan pesan rahasia : Pesan rahasia
```

Program akan menghasilkan `stego.png` yang berisi pesan tersembunyi.

## 5. Decode Pesan

Pilih menu:

```text
2
```

Kemudian masukkan path gambar stego.

Contoh:

```text
Masukkan gambar stego : images/stego.png
```

Program akan menampilkan pesan yang telah disisipkan.

## 6. Cek Kapasitas Gambar

Pilih menu:

```text
3
```

Kemudian masukkan path gambar.

Contoh:

```text
Masukkan path gambar: images/cover.png
```

Program akan menampilkan ukuran gambar dan kapasitas pesan yang dapat disisipkan.

## 7. Screen Shoot Running

<img width="982" height="602" alt="image" src="https://github.com/user-attachments/assets/29e70d86-251d-4839-adf6-b11a8d497750" />
<img width="772" height="488" alt="image" src="https://github.com/user-attachments/assets/a1557043-3510-4afd-8b11-4c515e995a0a" />
