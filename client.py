from networking import Client

if __name__ == "__main__":
    server_host = input("Enter server host: ")
    server_port = int(input("Enter server port: "))
    
    client = Client(host=server_host, port=server_port)
    client.start()
