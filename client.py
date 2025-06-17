
import sys

try:
    try:
        from Crypto.Cipher import AES
        from Crypto.Util.Padding import pad, unpad
    except ImportError:
            from Cryptodome.Cipher import AES
            from Cryptodome.Util.Padding import pad, unpad
except ImportError:
       print("please install required library pycryptodome")
       sys.exit(1)
    
import socket
import threading
import time
import base64
import hashlib


def get_aes_key(key):
    return hashlib.sha256(key.encode()).digest()

def encrypt_message(message):
    key = get_aes_key(SECRET_KEY)
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode()
    ct = base64.b64encode(ct_bytes).decode()
    return iv + ":" + ct

def decrypt_message(enc_message):
    try:
        key = get_aes_key(SECRET_KEY)
        iv, ct = enc_message.split(":")
        iv = base64.b64decode(iv)
        ct = base64.b64decode(ct)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return pt.decode()
    except:
        return "[!] Decryption Failed"

def banner():
    print("\033[92m")
    print(r"""
       _______               _______    _ _    
      |__   __|             |__   __|  | | |   
         | | ___ _ __ _ __ ___ | | __ _| | | __
         | |/ _ \ '__| '_ ` _ \| |/ _` | | |/ /
         | |  __/ |  | | | | | | | (_| | |   < 
         |_|\___|_|  |_| |_| |_|_|\__,_|_|_|\_\
                           
  
                            Developer: Sreeraj
 
           """)
    print("\033[92m  * GitHub : https://github.com/s-r-e-e-r-a-j\033[0m\n")
    
def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(2048).decode()
            if not msg:
                raise ConnectionError
            print(decrypt_message(msg))
        except:
            print("[!] Disconnected from server. Reconnecting...")
            sock.close()
            break

def connect_to_server(host, port, name):
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            print("[+] Connected to chat server.")
            sock.send(encrypt_message(f"{name} joined the chat").encode())
            threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

            while True:
                msg = input()
                if msg.lower() == "exit":
                    sock.send(encrypt_message(f"{name} exited the chat").encode())
                    sock.close()
                    return
                sock.send(encrypt_message(f"{name}: {msg}").encode())

        except Exception as e:
            print(f"[!] Connection failed: {e}")
            print("[*] Retrying in 5 seconds...")
            time.sleep(5)

def main():
    banner()
    print("=== Connect to  Chatroom ===")
    host = input("Enter HOST:").strip()
    port = int(input("Enter Server Port (e.g., 5000): "))
    global SECRET_KEY;
    SECRET_KEY=input("Enter The Secret Key (e.g., MyKey1234): ")
    SECRET_KEY=SECRET_KEY.strip()
    name = input("Your nickname: ")

    connect_to_server(host, port, name)

if __name__ == "__main__":
    main()
