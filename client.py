import socket
import threading
import time

def banner():
    print("""\033[92m

       _______               _______    _ _    
      |__   __|             |__   __|  | | |   
         | | ___ _ __ _ __ ___ | | __ _| | | __
         | |/ _ \ '__| '_ ` _ \| |/ _` | | |/ /
         | |  __/ |  | | | | | | | (_| | |   < 
         |_|\___|_|  |_| |_| |_|_|\__,_|_|_|\_\
                             
 
                            Developer: Sreeraj

      GitHub:https://github.com/s-r-e-e-r-a-j 
 
      \033[0m""")

def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            if not msg:
                raise ConnectionError
            print(msg)
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
            sock.send(f"{name} joined the chat".encode())
            threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

            while True:
                msg = input()
                if msg.lower() == "exit":
                    sock.send(f"{name} exited from the chat".encode())
                    sock.close()
                    return
                sock.send(f"{name}: {msg}".encode())

        except Exception as e:
            print(f"[!] Connection failed: {e}")
            print("[*] Retrying in 5 seconds...")
            time.sleep(5)

def main():
    banner()
    print("=== Connect to  Chatroom ===")
    host = input("Enter HOST:").strip()
    port = int(input("Enter Server Port (e.g., 12345): "))
    name = input("Your nickname: ")

    connect_to_server(host, port, name)

if __name__ == "__main__":
    main()
