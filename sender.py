import socket

ATTACKER_ADDRESS = ("localhost", 9090)
SENDER_ADDRESS   = ("localhost", 9091)

def recieve_flag():
    sock = socket.socket()
    sock.settimeout(5)
    sock.bind(SENDER_ADDRESS)
    sock.listen(1)
    try:
        conn, addr = sock.accept()
        print ('Соединение:', addr)
        data = conn.recv(100).decode("utf-8")
        conn.close()
        return data
    except socket.timeout:
        return None

def send_confirmation():
    sock = socket.socket()
    try:
        sock.connect(ATTACKER_ADDRESS)
        sock.send('flag recieved'.encode("utf-8"))
        sock.close()
        return True
    except ConnectionRefusedError:
        return False

def main():
    print("Ожидание флага...")
    while True:
        flag = recieve_flag()
        if flag and send_confirmation():
            break
        print("Ожидание...")
    print(f"Flag {flag} recieved!")

if __name__ == "__main__":
    main()