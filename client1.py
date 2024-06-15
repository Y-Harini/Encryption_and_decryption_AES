import socket
import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def socket_connection() :
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return client


def client_connect(client) :
    
    host = socket.gethostbyname(socket.gethostname())
    port = 9999
    client.connect((host, port))
    
    
def generate_key() :
    
    key = get_random_bytes(16)
    
    with open("generate_key.txt", "wb") as key_file :
        key_file.write(key)
    return key

def encrypt_data(file_name, key) :
    
    with open(file_name, "rb") as f :
        data = f.read()
        
    nonce = b"Sixteen byte key"
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    encrypted_data = cipher.encrypt(data)
    return encrypted_data


def send_files(client, file_name, encrypted_data) :
    
    file_size = os.path.getsize(file_name)
    client.send(file_name.encode("latin-1"))    
    client.send(str(file_size).encode("latin-1"))
    client.sendall(encrypted_data)
    client.send(b"<END>")
    client.close()

                                   #Main Program

    
client = socket_connection()
client_connect(client)
print("[CONNECTING] connected to client")
key = generate_key()
print(key)
file_name = "homeprices.csv"

encrypted_data = encrypt_data(file_name, key)
send_files(client, file_name, encrypted_data)
