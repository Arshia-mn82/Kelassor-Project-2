import socket
from abc import ABC, abstractmethod
import random

class NetworkEntity(ABC):
    def __init__(self, host='localhost', port=12345):
        self._host = host
        self._port = port
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    @abstractmethod
    def start(self):
        pass
    
    def _setup_socket(self):
        self._socket.bind((self._host, self._port))
        self._socket.listen(1)
    
    def _accept_connection(self):
        return self._socket.accept()

    def _connect(self):
        self._socket.connect((self._host, self._port))

class Server(NetworkEntity):
    def __init__(self, host='localhost', port=12345):
        super().__init__(host, port)
        self._secret_number = random.randint(1, 1000)
        print(f"Secret number: {self._secret_number}")

    def start(self):
        self._setup_socket()
        print(f"Server listening on {self._host}:{self._port}")
        while True:
            conn, addr = self._accept_connection()
            print(f"Connected by {addr}")
            with conn:
                self._handle_client(conn)

    def _handle_client(self, conn):
        while True:
            guess = conn.recv(1024).decode()
            if not guess:
                break
            try:
                guess = int(guess)
            except ValueError:
                conn.sendall(b"Invalid number")
                continue
            
            if guess < self._secret_number:
                conn.sendall(b"Too low")
            elif guess > self._secret_number:
                conn.sendall(b"Too high")
            else:
                conn.sendall(b"Correct")
                print("Client guessed the number correctly!")
                break

class Client(NetworkEntity):
    def __init__(self, host='localhost', port=12345):
        super().__init__(host, port)
    
    def start(self):
        self._connect()
        print("Connected to server.")
        while True:
            try:
                guess = int(input("Enter your guess (1-1000): "))
                if not (1 <= guess <= 1000):
                    print("Please enter a number between 1 and 1000.")
                    continue

                self._socket.sendall(str(guess).encode())
                response = self._socket.recv(1024).decode()
                print("Server response:", response)

                if response == "Correct":
                    print("Congratulations! You've guessed the number correctly.")
                    break
            except ValueError:
                print("Invalid input. Please enter a valid integer.")
