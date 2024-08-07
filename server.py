from networking import Server

if __name__ == "__main__":
    server = Server(host='localhost', port=12345)
    server.start()
