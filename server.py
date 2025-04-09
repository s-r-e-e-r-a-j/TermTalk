import socket
import threading
import subprocess
import os

# ANSI Colors
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
WHITE = "\033[97m"
RESET = "\033[0m"

clients = []


def banner():
    print("""\033[92m
             ===  Chatroom Server ===
       _______               _______    _ _    
      |__   __|             |__   __|  | | |   
         | | ___ _ __ _ __ ___ | | __ _| | | __
         | |/ _ \ '__| '_ ` _ \| |/ _` | | |/ /
         | |  __/ |  | | | | | | | (_| | |   < 
         |_|\___|_|  |_| |_| |_|_|\__,_|_|_|\_\
                              

                            Developer: Sreeraj

      GitHub:https://github.com/s-r-e-e-r-a-j 
 
      \033[0m""")



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
                print(f"""{YELLOW}[+] Serveo Public URL:{RESET}{GREEN}{url}{RESET} {CYAN} Use this in client:{RESET} {YELLOW}Host:{RESET}{GREEN} {host}{RESET} {YELLOW}Port:{RESET}{GREEN}{port}{RESET}""")
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
            message = client.recv(1024)
            if not message:
                break
            broadcast(message, client)
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
        print(f"""{YELLOW}[+] New client connected from IP: {ip}, Port: {port}{RESET}""")
        clients.append(client)
        threading.Thread(target=handle_client, args=(client,), daemon=True).start()

def main():
    os.system("clear" if os.name == "posix" else "cls");
    banner();
    bind_ip = input(f"{WHITE}Enter IP to bind to (e.g. 0.0.0.0 or 127.0.0.1): {RESET}").strip()
    port = int(input(f"{WHITE}Enter port to use (e.g. 5000): {RESET}"))

    threading.Thread(target=start_serveo_forwarding, args=(bind_ip, port), daemon=True).start()

    print(f"{GREEN}[*] Starting chat server...{RESET}\n")
    start_chat_server(bind_ip,port)

if __name__ == "__main__":
    main()
