import socket
from concurrent.futures import ThreadPoolExecutor
import time

class Sock:
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address

    def input(self):
        data = ""
        while True:
            buf = self.connection.recv(1024).decode()
            end_token = "\n"
            if end_token in buf:
                data += buf.split(end_token)[0]
                self.debug_print(data, sep=" >> ")
                return data
            else:
                buf += buf.decode()

    def output(self, data):
        self.debug_print(data, sep=" << ")
        self.connection.sendall(data.encode())

    def debug_print(self, data, sep=" << "):
        print(" | ".join(map(str, self.address)), sep, data)

    def sleep(self, seconds):
       self.output(f"⏰ Cooldown for {seconds} seconds\n")
       time.sleep(seconds)

    @classmethod
    def listen(self,sock_main, host="0.0.0.0", port=1337):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind((host, port))
        serversocket.listen()
        executor = ThreadPoolExecutor(max_workers=10)
        print(f"Listening on {host}:{port}...")
        while True:
            connection, address = serversocket.accept()
            print("Connection from", address)
            executor.submit(sock_main, Sock(connection, address))
