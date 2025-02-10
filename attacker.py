import json, requests, os, socket

OFFLINE          = True
ATTACKER_ADDRESS = ("localhost", 9090)
SENDER_ADDRESS   = ("localhost", 9091)


def request_task(surname, name):
    print("Запрос заданий для выполнения...")
    if OFFLINE:
        response = {'variant': 1, 'tasks' : [], 'flag': 'flag{test}'}
    else:
        url      = "http://172.18.4.200:8080/api/start"
        payload  = {
            "username":   surname + "_" + name,
            "pnet_login": "",
            "lab":        "Cain&Abel ARP Poisoning",
            "lab_slug":   "cain-and-abel-arp-poisoning",
        }
        payload           = json.dumps(payload).encode('utf-8')
        response          = requests.request("GET", url, data=payload)
        response.encoding = 'utf-8'
        response          = json.loads(response.text)
    for i in ['variant', 'tasks', 'flag']:
        if i not in response.keys():
            print("Ошибка получения заданий для выполнения!\n", response)
            exit()
    return response


def finish_task(surname, name):
    if OFFLINE:
        response = "Offline mode: task is finished"
    else:
        url     = "http://172.18.4.200:8080/api/end"
        payload = {
            "username":   surname + "_" + name,
            "pnet_login": "",
            "lab":        "Cain&Abel ARP Poisoning",
            "lab_slug":   "cain-and-abel-arp-poisoning"
        }
        payload           = json.dumps(payload).encode('utf-8')
        response          = requests.request("POST", url, data=payload)
        response.encoding = 'utf-8'
        response          = json.loads(response.text)
    return response


def send_flag(flag):
    sock = socket.socket()
    try:
        sock.connect(SENDER_ADDRESS)
        sock.send(flag.encode("utf-8"))
        sock.close()
        return True
    except ConnectionRefusedError:
        print("Не удалось отправить флаг!")
        return False


def wait_for_confirmation():
    sock = socket.socket()
    sock.settimeout(5)
    sock.bind(ATTACKER_ADDRESS)
    sock.listen(1)
    try:
        conn, addr = sock.accept()
        print ('Соединение:', addr)
        data = conn.recv(100).decode("utf-8")
        print(data)
        conn.close()
        if data == 'flag recieved':
            print("Подтверждение получено!")
            return True
        print("Подтверждение не получено!")
        return False
    except socket.timeout:
        print("Ответ не получен!")
        return False

def read_and_check_flag(correct_flag):
    flag = input("Введите флаг: ")
    if flag == correct_flag:
        print("Флаг введен верно!")
        return True
    print("Флаг введен неверно!") 
    return False


def main():
    surname      = input("Введите Фамилию: ")
    name         = input("Введите Имя:     ")
    response     = request_task(surname, name)
    correct_flag = response['flag']

    print("Настройка сети...")
    while True:
        if send_flag(correct_flag) and wait_for_confirmation():
            break
        print("Ожидание...")
    print("Cеть настроена!")
    
    while True:
        if read_and_check_flag(correct_flag):
            break
    
    finish_task(surname, name)
    print("Задание выполнено!")
    input()
    

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nВыполнение работы прервано!")