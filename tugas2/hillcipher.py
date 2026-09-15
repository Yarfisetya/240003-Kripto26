import math

MODULUS = 26


def text_to_numbers(text):
    text = text.upper().replace(" ", "")

    if not text.isalpha() or not text.isascii():
        raise ValueError("Teks hanya boleh berisi huruf A-Z.")

    return [ord(char) - ord("A") for char in text]


def numbers_to_text(numbers):
    return "".join(chr((number % MODULUS) + ord("A")) for number in numbers)


def input_key():
    order = int(input("Masukkan ordo matriks key: "))

    if order < 2:
        raise ValueError("Ordo matriks minimal 2.")

    key = []

    print(f"Masukkan key {order} x {order}:")

    for i in range(order):
        row = list(map(int, input(f"Baris {i + 1}: ").split()))

        if len(row) != order:
            raise ValueError(
                f"Setiap baris harus memiliki {order} angka."
            )

        key.append([value % MODULUS for value in row])

    return key


def determinant(matrix):
    size = len(matrix)

    if size == 1:
        return matrix[0][0]

    if size == 2:
        return (
            matrix[0][0] * matrix[1][1]
            - matrix[0][1] * matrix[1][0]
        )

    result = 0

    for column in range(size):
        minor = [
            [
                matrix[row][item]
                for item in range(size)
                if item != column
            ]
            for row in range(1, size)
        ]

        sign = 1 if column % 2 == 0 else -1

        result += (
            sign
            * matrix[0][column]
            * determinant(minor)
        )

    return result


def modular_inverse(number):
    number %= MODULUS

    for candidate in range(MODULUS):
        if (number * candidate) % MODULUS == 1:
            return candidate

    raise ValueError("Invers modulo tidak ditemukan.")


def validate_key(key):
    det = determinant(key) % MODULUS

    if math.gcd(det, MODULUS) != 1:
        raise ValueError(
            "Key tidak valid karena determinannya "
            "tidak relatif prima dengan 26."
        )


def inverse_key(key):
    validate_key(key)

    size = len(key)

    # Untuk matriks 2x2
    if size == 2:
        a = key[0][0]
        b = key[0][1]
        c = key[1][0]
        d = key[1][1]

        det = (a * d - b * c) % MODULUS
        det_inverse = modular_inverse(det)

        inverse = [
            [
                d * det_inverse % MODULUS,
                -b * det_inverse % MODULUS
            ],
            [
                -c * det_inverse % MODULUS,
                a * det_inverse % MODULUS
            ]
        ]

        return inverse

    raise ValueError(
        "Pencarian invers saat ini digunakan untuk key 2x2."
    )


def multiply_matrix_vector(matrix, vector):
    size = len(matrix)

    result = []

    for row in range(size):
        total = 0

        for column in range(size):
            total += matrix[row][column] * vector[column]

        result.append(total % MODULUS)

    return result


def process_text(text, key):
    numbers = text_to_numbers(text)

    block_size = len(key)

    # Tambahkan X jika jumlah huruf tidak habis dibagi ukuran key
    while len(numbers) % block_size != 0:
        numbers.append(ord("X") - ord("A"))

    result = []

    for index in range(0, len(numbers), block_size):
        block = numbers[index:index + block_size]

        encrypted_block = multiply_matrix_vector(
            key,
            block
        )

        result.extend(encrypted_block)

    return numbers_to_text(result)


def encryption():
    plain_text = input("Masukkan plaintext: ")

    key = input_key()

    validate_key(key)

    cipher_text = process_text(plain_text, key)

    print("CIPHERTEXT:", cipher_text)


def decryption():
    cipher_text = input("Masukkan ciphertext: ")

    key = input_key()

    inverse = inverse_key(key)

    plain_text = process_text(cipher_text, inverse)

    print("PLAINTEXT:", plain_text)


def multiply_matrix(left, right):
    size = len(left)

    result = []

    for row in range(size):
        new_row = []

        for column in range(size):
            total = 0

            for item in range(size):
                total += (
                    left[row][item]
                    * right[item][column]
                )

            new_row.append(total % MODULUS)

        result.append(new_row)

    return result


def find_key():
    order = int(input("Masukkan ordo matriks key: "))

    if order != 2:
        raise ValueError(
            "Fitur mencari key dibuat untuk matriks 2x2."
        )

    plain_text = input(
        "Masukkan 4 huruf plaintext yang diketahui: "
    )

    cipher_text = input(
        "Masukkan 4 huruf ciphertext pasangannya: "
    )

    plain_numbers = text_to_numbers(plain_text)
    cipher_numbers = text_to_numbers(cipher_text)

    if len(plain_numbers) != 4 or len(cipher_numbers) != 4:
        raise ValueError(
            "Plaintext dan ciphertext harus tepat 4 huruf."
        )

    # Membentuk matriks plaintext
    plain_matrix = [
        [plain_numbers[0], plain_numbers[2]],
        [plain_numbers[1], plain_numbers[3]]
    ]

    # Membentuk matriks ciphertext
    cipher_matrix = [
        [cipher_numbers[0], cipher_numbers[2]],
        [cipher_numbers[1], cipher_numbers[3]]
    ]

    plain_inverse = inverse_key(plain_matrix)

    key = multiply_matrix(
        cipher_matrix,
        plain_inverse
    )

    print("KEY:")

    for row in key:
        print(*row)


def menu():
    print()
    print("===== HILL CIPHER =====")
    print("1. Enkripsi")
    print("2. Dekripsi")
    print("3. Cari Kunci")
    print("4. Keluar")

    return input("Masukkan pilihan: ")


def main():
    while True:
        pilihan = menu()

        try:
            if pilihan == "1":
                encryption()

            elif pilihan == "2":
                decryption()

            elif pilihan == "3":
                find_key()

            elif pilihan == "4":
                print("Program selesai.")
                break

            else:
                print("Pilihan tidak valid.")

        except ValueError as error:
            print("Error:", error)


if __name__ == "__main__":
    main()