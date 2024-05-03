import argparse
import os
import socket

def ls(conn, directory='.'):
    parser = argparse.ArgumentParser(description='List files in a directory')
    parser.add_argument('directory', type=str, nargs='?', default='.')
    args = parser.parse_args()

    files = os.listdir(args.directory)
    files_str = '\n'.join(files)
    conn.sendall(files_str.encode('utf-8'))

def remove_file(filename):
    if os.path.exists(filename):
        os.remove(filename)
        return "File {} has been removed.".format(filename)
    else:
        return "File {} does not exist.".format(filename)

# Fungsi upload
def upload(conn, filename, upload_dir='.'):
    try:
        # Memastikan upload_dir adalah path absolut
        upload_dir = os.path.abspath(upload_dir)
        
        # Membuat direktori upload_dir jika belum ada
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        
        # Menentukan lokasi file tujuan
        file_destination = os.path.join(upload_dir, filename)
        
        # Memeriksa apakah file sudah ada di lokasi tujuan
        if os.path.exists(file_destination):
            user_input = input("File {} sudah tersedia di {}. Apakah Anda ingin menggantinya? (y/n): ".format(filename, upload_dir))
            if user_input.lower() != 'y':
                return "Upload dibatalkan. File {} tidak diunggah.".format(filename)
        
        # Membuka file untuk ditulis dalam mode binary
        with open(file_destination, 'wb') as f:
            # # Menerima data dari koneksi dan menulisnya ke file
            # while True:
            #     data = conn.recv(1024)
            #     if not data:
            #         break
            #     f.write(data)
        
        # Mengembalikan pesan sukses dengan lokasi file yang diunggah
            file_location = os.path.join(upload_dir, filename)
        return "File {} telah diunggah ke {}.".format(filename, file_location)
    except Exception as e:
        # Mengembalikan pesan error jika terjadi kesalahan
        error_message = "Terjadi kesalahan saat mengunggah {}: {}".format(filename, str(e))
        print(error_message)
        return error_message

        
def download(conn, filename, download_dir='.'):
    try:
        # Memastikan download_dir adalah path absolut
        download_dir = os.path.abspath(download_dir)
        
        # Membuka file untuk dibaca dalam mode binary
        with open(os.path.join(download_dir, filename), 'rb') as f:
            # Membaca data dari file dan mengirimkannya ke koneksi
            data = f.read(1024)
            while data:
                conn.sendall(data)
                data = f.read(1024)
        
        # Mengembalikan pesan sukses dengan lokasi file yang diunduh
        file_location = os.path.join(download_dir, filename)
        file_size = os.path.getsize(file_location)
        return "File {} ({} bytes) has been downloaded from {}".format(filename, file_size, file_location)
    except Exception as e:
        # Mengembalikan pesan error jika terjadi kesalahan
        error_message = "Terjadi kesalahan saat mengunduh {}: {}".format(filename, str(e))
        print(error_message)
        return error_message



def convert_size(size_bytes):
    # Daftar unit ukuran file dalam urutan terbesar ke terkecil
    units = ['B', 'KB', 'MB', 'GB', 'TB']

    # Loop melalui daftar unit dan konversi ukuran byte ke unit yang sesuai
    for unit in units:
        if size_bytes < 1024:
            if unit == 'B':
                return "{} {}".format(int(size_bytes), unit)
            else:
                return "{:.2f} {}".format(size_bytes, unit)
        size_bytes /= 1024

    return "{:.2f} {}".format(size_bytes, units[-1])

def get_file_size(filename):
    if os.path.exists(filename):
        size_bytes = os.path.getsize(filename)
        return convert_size(size_bytes)
    else:
        return "File {} does not exist.".format(filename)




def handle_client(conn):
    while True:
        data = conn.recv(1024).decode('utf-8')
        # if not data:
        #     break

        command = data.split()
        if command[0] == 'ls':
            ls(conn, command[1] if len(command) > 1 else '.')
        elif command[0] == 'rm':
            if len(command) > 1:
                response = remove_file(command[1])
            else:
                response = "Usage: rm [filename]"
            conn.sendall(response.encode('utf-8'))    
        elif command[0] == 'upload':
            if len(command) > 1:
             filename = command[1]
             upload_dir = input("Masukkan direktori tempat file akan diunggah (biarkan kosong untuk direktori saat ini): ")

            if not os.path.exists(upload_dir):
                print("Direktori yang dimasukkan tidak valid atau tidak dapat diakses.")
                response = "Error: Direktori tidak valid atau tidak dapat diakses."
            else:
                 response = upload(conn, filename, upload_dir)
        
            conn.sendall(response.encode('utf-8'))

        elif command[0] == 'download':
            if len(command) > 1:
                filename = command[1]
                response = download(conn, filename)
            else:
                response = "Usage: download [filename]"
            conn.sendall(response.encode('utf-8'))
        elif command[0] == 'size':
            if len(command) > 1:
                filename = command[1]
                response = get_file_size(filename)
            else:
                response = "Usage: size [filename]"
            conn.sendall(response.encode('utf-8'))
        elif command[0] == 'byebye':
            response = "Goodbye!"
            conn.sendall(response.encode('utf-8'))
            conn.close()
            break
        elif command[0] == 'connme':
            response = "Connection established successfully."
            conn.sendall(response.encode('utf-8'))
        else:
            response = "Invalid command."
            conn.sendall(response.encode('utf-8'))


def main():
    HOST = '127.0.0.1'
    PORT = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        print("Server listening on port", PORT)

        while True:
            conn, addr = server_socket.accept()
            print('Connected by', addr)
            handle_client(conn)

if __name__ == "__main__":
    main()