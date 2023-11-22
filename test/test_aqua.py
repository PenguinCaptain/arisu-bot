import requests

card = "26472970039944107244"

import socket
from typing import reveal_type

from Crypto.Cipher import AES

key = "Copyright(C)SEGA".encode(encoding="utf-8")
cipher = AES.new(key, AES.MODE_ECB)


class AimeDB:
    def __init__(self, url="114.132.74.203", port=22345):
        self.url = url
        self.port = port

    def register_user_id(self, access_code):
        if len(access_code) != 20 or not access_code.isdigit():
            return False

        # create a byte array with the size of 48 bytes
        # replace the first 8 bytes with 3E A1 87 30 05 00 30 00
        # replace the 10 bytes from 0x20 with the hex representation of the access code

        byte_array = bytearray(48)
        byte_array[0:8] = bytearray.fromhex("3E A1 87 30 05 00 30 00")
        byte_array[0x20:0x2A] = bytearray.fromhex(access_code)

        recv_data = self._send_data(byte_array)
        # read status code from 0x08
        status_code = recv_data[0x08]
        if status_code == 1:
            # read user id from 0x20 in 4 bytes Long Little Endian
            user_id = int.from_bytes(recv_data[0x20:0x24], byteorder="little")
            return user_id
        else:
            return False

    def get_user_id(self, access_code):
        if len(access_code) != 20 or not access_code.isdigit():
            return False

        byte_array = bytearray(48)
        byte_array[0:8] = bytearray.fromhex("3E A1 87 30 04 00 30 00")
        byte_array[0x20:0x2A] = bytearray.fromhex(access_code)

        recv_data = self._send_data(byte_array)

        user_id = int.from_bytes(recv_data[0x20:0x24], byteorder="little", signed=True)

        if user_id < 0:
            return False

        return user_id

    def _send_data(self, data):
        encrypted_data = cipher.encrypt(data)

        # Establish a TCP socket with the host "HOSTNAME" and the port 22345
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.url, self.port))
            s.sendall(encrypted_data)

            received_data = s.recv(1024)  # adjust buffer size if needed

        # Decrypt the received data
        decrypted_data = cipher.decrypt(received_data)
        return decrypted_data