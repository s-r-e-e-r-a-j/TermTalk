## TermTalk
**TermTalk** is a terminal-based chatroom application built with Python. It allows multiple users to chat with each other over the internet using a simple client-server setup.

## Features
- Real-time chat between multiple users
- Simple terminal interface
- Works over the internet using Serveo.net tunneling
- Automatic reconnection support for clients
- Colored banner and messages for a cool terminal vibe
- Lightweight and easy to use
- Supports Linux and Termux 

## Requirements
- Python 3.x
- OpenSSH (for Serveo tunnel)
- Internet connection
- Linux or Termux (Android terminal emulator)

## How to Use

**1. On the Server**

```bash
python3 server.py
```
- Enter the IP to bind (e.g., 192.168.1.7) The ipaddress of your system 

- Enter a port (e.g., 5000)

- A public URL will be generated using Serveo (e.g., serveo.net:12345)

**2. On the Client**

```bash
python3 client.py
```
- Enter the Host (e.g., serveo.net)

- Enter the Port (e.g., 12345)

- Enter your nickname

- Start chatting!

  To exit the chat, type `exit`.

 ## Example
**Server Output:**

```css
[+] Serveo Public URL: serveo.net:12345
```

**Client Input:**

```yaml
Enter HOST: serveo.net
Enter Server Port: 12345
Your nickname: allah
```

## Developer
- Sreeraj
- GitHub: https://github.com/s-r-e-e-r-a-j

  

