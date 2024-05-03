import socket

def main():
    HOST = '127.0.0.1'  
    PORT = 12345        

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        print("Connected to server.")

        while True:
            command = input("Enter command: ")

            if command.lower() == 'exit':
                client_socket.sendall(command.encode('utf-8'))
                break

            client_socket.sendall(command.encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            print("Response:", response)

if __name__ == "__main__":
    main()
