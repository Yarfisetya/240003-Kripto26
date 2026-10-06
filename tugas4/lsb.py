from PIL import Image


HEADER_SIZE = 32


def text_to_bytes(text):
    return text.encode("utf-8")


def bytes_to_bits(data):
    bits = []

    for byte in data:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)

    return bits


def bits_to_bytes(bits):
    data = bytearray()

    for i in range(0, len(bits), 8):
        byte = 0

        for bit in bits[i:i + 8]:
            byte = (byte << 1) | bit

        data.append(byte)

    return bytes(data)


def int_to_bits(number):
    bits = []

    for i in range(31, -1, -1):
        bits.append((number >> i) & 1)

    return bits


def bits_to_int(bits):
    number = 0

    for bit in bits:
        number = (number << 1) | bit

    return number


def get_capacity(image):
    width, height = image.size

    # Setiap pixel menggunakan 3 channel:
    # R, G, B
    return width * height * 3


def encode(image_path, message, output_path):
    image = Image.open(image_path).convert("RGBA")

    message_bytes = text_to_bytes(message)

    # Header menyimpan panjang pesan dalam byte
    length_bits = int_to_bits(len(message_bytes))

    # Pesan diubah menjadi bit
    message_bits = bytes_to_bits(message_bytes)

    # Gabungkan header + pesan
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

                # Ubah LSB channel menjadi bit pesan
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


def decode(image_path):
    image = Image.open(image_path).convert("RGBA")

    pixels = image.load()

    # Ambil 32 bit pertama sebagai panjang pesan
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

    # Jumlah bit pesan
    message_bit_count = message_length * 8

    message_bits = []

    bit_count = 0

    for y in range(image.height):
        for x in range(image.width):

            r, g, b, a = pixels[x, y]

            channels = [r, g, b]

            for channel in channels:

                # Lewati 32 bit header
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