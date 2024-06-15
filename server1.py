import socket
import tqdm
from Crypto.Cipher import AES

def socket_connection() :
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return server


def socket_bind(server) :
    
    host = socket.gethostbyname(socket.gethostname())
    port = 9999
    server.bind((host, port))
    server.listen()
    
    
def decrypt_data(server) :
    
    conn, addr = server.accept()
    print(f"[NEW CONNECTION] new connection {addr} accepted")
    
    file_name = conn.recv(14).decode("latin-1")
    print(f"file name : {file_name}")
    
    file_size = conn.recv(3).decode("latin-1")
    print(f"file size : {file_size}")

    with open("generate_key.txt", "rb") as data :
        key = data.read()
        
    nonce = b"Sixteen byte key"  
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    
    
    file = open("decrypted_data.txt", "wb")
    done = False
    file_bytes = b""
    progress = tqdm.tqdm(unit = "B", unit_scale=True, unit_divisor=1000, total = int(file_size))
    
    while not done :

        file_data = conn.recv(1024)
        
        if file_bytes[-5:] == b"<END>" :
            done = True
            
        else :
            file_bytes += file_data
            
        progress.update(1024)  
            
    file.write(cipher.decrypt(file_bytes[:-5]))
    file.close()
    conn.close()

                                    #Main Program

    
server = socket_connection()
socket_bind(server)
print("[LISTENING] server is listening")
decrypt_data(server)
print("Data is decrypted")
    
    
    

