def main():
    HOST = '127.0.0.1'
    PORT = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        print("Connected to server.")

        client_socket.sendall('connme'.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        print(response)
        while True:
            command = input("Enter command: ")
            client_socket.sendall(command.encode('utf-8'))

            if command == 'byebye':
                print("Closing connection.")
                break

            response = client_socket.recv(4096).decode('utf-8')
            print(response)
            
            while "Continue" in response:
                response = client_socket.recv(4096).decode('utf-8')
                print(response)


   

if __name__ == "__main__":
    main()