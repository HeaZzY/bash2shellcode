def encode_string(s: str, xor_key: int = 0x00) -> tuple[list[int], int]:
    """
    Encode une chaîne en valeurs numériques XORées.
    Retourne les valeurs encodées et la longueur.
    """
    print("[+] s : ", s)
    padded = s.encode() + b'\x00' * (8 - (len(s) % 8))
    length = len(s)

    encoded = [b ^ xor_key for b in padded]

    values = []
    for i in range(0, len(encoded), 8):
        chunk = encoded[i:i+8]
        value = int.from_bytes(bytes(chunk), 'little')
        print("[+] value : ", hex(value))
        values.append(value)

    return values, len(values)*8


print(encode_string("uname -a", 0x01))
