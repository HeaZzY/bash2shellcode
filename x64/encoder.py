def encode_string(s: str) -> tuple[list[int], int]:

    padded = s.encode() + b'\x00' * (8 - (len(s) % 8))
    length = len(s)

    encoded = [b  for b in padded]

    values = []
    for i in range(0, len(encoded), 8):
        chunk = encoded[i:i+8]
        value = int.from_bytes(bytes(chunk), 'little')
        values.append(value)

    return values, len(values)*8