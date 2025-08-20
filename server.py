#!/usr/bin/env python3

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
import subprocess
import os
import base64
import hashlib

# ANSI Colors
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
WHITE = "\033[97m"
RESET = "\033[0m"

clients = []

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
             ===  Chatroom Server ===
       _______               _______    _ _    
      |__   __|             |__   __|  | | |   
         | | ___ _ __ _ __ ___ | | __ _| | | __
         | |/ _ \ '__| '_ ` _ \| |/ _` | | |/ /
         | |  __/ |  | | | | | | | (_| | |   < 
         |_|\___|_|  |_| |_| |_|_|\__,_|_|_|\_\
                              

                            Developer: Sreeraj

          """)
    print("\033[92m  * GitHub : https://github.com/s-r-e-e-r-a-j\033[0m\n")

def start_serveo_forwarding(bind_ip, port):
    print(f"{GREEN}[*] Starting Serveo tunnel...{RESET}")
    proc = subprocess.Popen(
        ["ssh", "-o", "StrictHostKeyChecking=no", "-R", f"0:{bind_ip}:{port}", "serveo.net"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        line = line.strip()
        if "Forwarding TCP connections from" in line:
            url = line.split("from")[-1].strip()
            if "serveo.net:" in url:
                host, port = url.split(":")
                print(f"""{CYAN}[+] Use this in client:{RESET} {YELLOW}Host:{RESET}{GREEN} {host}{RESET} {YELLOW}Port:{RESET}{GREEN}{port} {YELLOW}Secret Key:{RESET}{GREEN}{SECRET_KEY}{RESET}""")
            break
 
def broadcast(message, sender):
    for client in clients:
        if client != sender:
            try:
                client.send(message)
            except:
                clients.remove(client)

def handle_client(client):
    while True:
        try:
            enc_message = client.recv(2048)
            if not enc_message:
                break
            decrypted_msg = decrypt_message(enc_message.decode())
            if decrypted_msg == "[!] Decryption Failed":
                client.send(encrypt_message("[!] Invalid Secret Key. Connection closing...").encode())
                clients.remove(client)
                client.close()
                break
            # Re-encrypt before broadcasting
            broadcast(encrypt_message(decrypted_msg).encode(), client)
        except:
            if client in clients:
                clients.remove(client)
            client.close()
            break


def start_chat_server(ip, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen()
    print(f"\n{GREEN}[+] Chat server started on {ip}:{port}{RESET}\n")
    while True:
        client, addr = server.accept()
        ip, port = addr
        print(f"{YELLOW}[+] New client connected from IP: {ip}, Port: {port}{RESET}")
        clients.append(client)
        threading.Thread(target=handle_client, args=(client,), daemon=True).start()

def main():
    try:
        os.system("clear" if os.name == "posix" else "cls")
        banner()
        bind_ip = input(f"{WHITE}Enter IP to bind to [your IP] (e.g. 192.168.1.7): {RESET}").strip()
        port = int(input(f"{WHITE}Enter port to use (e.g. 5000): {RESET}"))
        global SECRET_KEY
        SECRET_KEY=input(f"{WHITE}Enter A Secret Key (e.g. MyKey1234): {RESET}");
        SECRET_KEY=SECRET_KEY.strip();
        threading.Thread(target=start_serveo_forwarding, args=(bind_ip, port), daemon=True).start();
        print(f"{GREEN}[*] Starting chat server...{RESET}\n")
        start_chat_server(bind_ip, port)

    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)

if __name__ == "__main__":
    main()
