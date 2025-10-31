## TermTalk
**TermTalk** is a terminal-based chatroom application built with Python. It allows multiple users to chat with each other over the internet using a simple client-server setup.

## Features
- Real-time chat between multiple users
- Simple terminal interface
- Works over the internet using Serveo.net tunneling
- Automatic reconnection support for clients
- Lightweight and easy to use
- Supports Linux and Termux
- All messages are secured with strong AES encryption, ensuring privacy.
- **Messages are sent and received only by the clients. The server acts solely as an intermediary to route messages between clients.**

## Requirements

- **Python 3.x**  
  Make sure Python 3 is installed on your system.
  
- **OpenSSH**  
  Required for Serveo tunnel to establish remote connections.

- **Internet Connection**  
  Required to use Serveo and for general network communication between clients and servers.

- **Linux or Termux**  
  Works on various Linux distributions (e.g., Debian, RHEL, Arch) and Termux (for Android).

- **PyCryptodome**  
  Required for AES encryption support. Install it using:

```bash
  pip3 install pycryptodome
```
**Note for Kali, Parrot, Ubuntu 23.04+ users:**

If you see an error like:
```go
error: externally-managed-environment
```
then use:
```bash
pip3 install pycryptodome --break-system-packages
```
## How to Use

**1. On the Server**

```bash
python3 server.py
```
- Enter the IP to bind (e.g., 192.168.1.7) The ipaddress of your system 

- Enter a port (e.g., 5000)
- Enter a secret key (eg., MyKey1234)
- Once the server is running, you'll see the following connection information:
```css
[+] Use this in client: Host: serveo.net Port: 47056 Secret Key: MyKey1234
```
This provides the **Host**, **Port**, and **Secret Key** needed for clients to connect securely.

**2. On the Client**

```bash
python3 client.py
```
- Enter the Host (e.g., serveo.net)

- Enter the Port (e.g., 12345)
  
- Enter The Secret Key (e.g., MyKey1234)

- Enter your nickname

- Start chatting!

  To exit the chat, type `exit`.

 ## Example
**Server Output:**

```css
[+] Use this in client: Host: serveo.net Port: 47056 Secret Key: MyKey1234
```

**Client Input:**

```yaml
Enter HOST: serveo.net
Enter Server Port: 12345
Enter The Secret Key (e.g., MyKey1234): MyKey1234
Your nickname: allah
```
## License
This project is licensed under the MIT License
