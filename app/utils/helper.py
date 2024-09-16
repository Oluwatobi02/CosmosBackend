import secrets

def gen_random_byte_hex(length=12):
    return secrets.token_hex(length)

def get_hex_hash(hexlst: list[str]):
    hex1, hex2 = hexlst
    num1 = int(hex1, 16)
    num2 = int(hex2, 16)
    sum_ = num1 + num2
    return hex(sum_)[2:]