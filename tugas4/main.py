from lsb import encode, decode, get_capacity
from PIL import Image


def show_capacity():
    image_path = input("Masukkan path gambar: ")

    try:
        image = Image.open(image_path)

        capacity = get_capacity(image)

        # 32 bit digunakan untuk menyimpan panjang pesan
        max_bytes = (capacity - 32) // 8

        print("\nInformasi Gambar")
        print("------------------------")
        print(f"Ukuran gambar : {image.width} x {image.height}")
        print(f"Kapasitas bit : {capacity} bit")
        print(f"Kapasitas pesan : {max_bytes} byte")

    except Exception as e:
        print(f"Error: {e}")


def encode_menu():
    image_path = input("Masukkan gambar cover : ")
    output_path = input("Masukkan nama output : ")
    message = input("Masukkan pesan rahasia : ")

    try:
        encode(
            image_path,
            message,
            output_path
        )

        print("\nPesan berhasil disembunyikan!")
        print(f"Stego image : {output_path}")

    except Exception as e:
        print(f"\nGagal melakukan encode: {e}")


def decode_menu():
    image_path = input("Masukkan gambar stego : ")

    try:
        message = decode(image_path)

        print("\nPesan tersembunyi:")
        print("------------------------")
        print(message)

    except Exception as e:
        print(f"\nGagal melakukan decode: {e}")


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


if __name__ == "__main__":
    main()