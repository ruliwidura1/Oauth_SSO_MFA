# Berikut adalah contoh kode sederhana untuk menghasilkan Time-Based One-Time Password (TOTP) menggunakan Python tanpa menggunakan pustaka
# eksternal seperti 'Pyotp'. kode ini mengimolementasikan algoritma TOTP berdasarkan RFC 6238.

import hmac
import hashlib
import struct
import time

def generate_totp(secret, time_step=30, digits=6):
    # Hitung waktu opech yang di bagi dengan time_step
    curent_bytes = int(time.time()) // time_step

    # Konversi curent_time menjadi byte array (big_endian).
    time_bytes = struct.pack(">Q", current_time)

    # Hitung HMAC-SHA1 dari secret key dan current_time
    hmac_result = hmac.new(secret.encode('utf-8'), time_bytes,hashlib.sha1)

    # Ambil 4-byte terakhir dari HMAC result sebagai offset
    offset = hmac_result[-1] & 0X0F

    # Ambil 4-byte dari HMAC result dari mulai offset
    truncated_hash = hmac_result[offset:offset + 4]

     # Konversi hasil menjadi integer.
    binary = struct.unpack(">I", truncated_hash)[0]

    # Hapus digit paling signifikan.
    binary &= 0x7FFFFFFF

    # Ambil modulus dengan 10^digits.
    otp = str(binary % (10 ** digits))

    # Tambahkan nol di depan jika panjangnya kurang dari digits.
    while len(otp) < digits:
        otp = "0" + otp

    return otp

# Secret key yang dibagikan dengan perangkat yang memerlukan TOTP.
secret_key = 'JBSWY3DPEHPK3PXP'

# Generate dan cetak TOTP code.
totp_code = generate_totp(secret_key)
print(f"Current TOTP Code: {totp_code}")
