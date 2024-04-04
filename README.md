``` sh
Nama : Afifah Fikriyah 
NIM : 1203220051 
```

# Soal 

- buat sebuah program file transfer protocol menggunakan socket programming dengan beberapa perintah dari client seperti berikut
ls : ketika client menginputkan command tersebut, maka server akan memberikan daftar file dan folder 
rm {nama file} : ketika client menginputkan command tersebut, maka server akan menghapus file dengan acuan nama file yang diberikan pada parameter pertama
download {nama file} : ketika client menginputkan command tersebut, maka server akan memberikan file dengan acuan nama file yang diberikan pada parameter pertama
upload {nama file} : ketika client menginputkan command tersebut, maka server akan menerima dan menyimpan file dengan acuan nama file yang diberikan pada parameter pertama
size {nama file} : ketika client menginputkan command tersebut, maka server akan memberikan informasi file dalam satuan MB (Mega bytes) dengan acuan nama file yang diberikan pada parameter pertama
byebye : ketika client menginputkan command tersebut, maka hubungan socket client akan diputus
connme : ketika client menginputkan command tersebut, maka hubungan socket client akan terhubung. 

- buat readme.md dengan memberikan Nama dan nim serta penjelasan dan cara menggunakan setiap command yang tersedia
penilaian
50% : program
50% : readme

- Upload di github dan kumpulkan url repositorinya

# Penjelasan Program 

1. command ls 
```sh
def ls(conn, directory='.'):
    parser = argparse.ArgumentParser(description='List files in a directory')
    parser.add_argument('directory', type=str, nargs='?', default='.')
    args = parser.parse_args()

    files = os.listdir(args.directory)
    files_str = '\n'.join(files)
    conn.sendall(files_str.encode('utf-8'))

```

berada dalam server.py di mana ls berfungsi untuk mengirim daftar list file dan folder dalam direktori tersebut, prosesnya mencakup: 

1. Fungsi yang menerima parameter conn sebagai socket dan directory untuk memeriksa isi dari suatu direktori
2. Membuat objek ArgumentParser untuk mengelola argumen baris perintah dengan deskripsi "List files in a directory"
3. Menambahkan argumen directory yang opsional ke parser. Argumen ini menunjukkan direktori yang ingin ditampilkan dan defaultnya adalah direktori saat ini ('.')
4. args = parser.parse_args(): Mem-parsing argumen dari baris perintah yang diberikan oleh pengguna
5. files = os.listdir(args.directory): Mendapatkan daftar file dalam direktori yang ditentukan dari argumen baris perintah
6. files_str = '\n'.join(files): Menggabungkan daftar nama file menjadi satu string dengan baris baru di antara setiap nama file
7. conn.sendall(files_str.encode('utf-8')): Mengirim string yang berisi daftar file ke koneksi yang diberikan.

output yang dihasilkan dari pemanggilan command ls:

[reference images](assets/ls%20output.png)

2. command rm 

```sh
def remove_file(filename):
    if os.path.exists(filename):
        os.remove(filename)
        return "File {} has been removed.".format(filename)
    else:
        return "File {} does not exist.".format(filename)

```

command rm berfungsi untuk menghapus sebuah file yang ada di dalam direktori, pertamanya akan mengecek apakah path yang dituju ada ( dibantu dengan library os yang disediakan oleh python) ketika file yang dicari ada maka akan menghapus file tersebut jika tidak maka akan mengembalikan pesan file does not exist 

[reference images](assets/rm.png)

3. command download 

```sh
def download(conn, filename):
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            data = f.read(1024)
            while data:
                conn.sendall(data)
                data = f.read(1024)
        return "File {} has been downloaded.".format(filename)
    else:
        return "File {} does not exist.".format(filename)
```

command download berfungsi untuk mendownload sebuah file ( membaca file yang dituju ) 

[reference images](assets/download.png)

4. command upload 

```sh
def upload(conn, filename):
    with open(filename, 'wb') as f:
        data = conn.recv(1024)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            f.write(data)
    print("File {} has been uploaded.".format(filename))
```

command upload berfungsi untuk mengupload sebuah file yang akan dibuat, dalam program ini masih terdapat bug di saat file berhasil diupload koneksi antar socket, namun program ini sudah bisa mengupload file dengan berhasil 

[reference images](assets/upload.png) 
[reference images](assets/kondisiupload.png)

5. command size 

```sh
def get_file_size(filename):
    if os.path.exists(filename):
        size_bytes = os.path.getsize(filename)
        return str(size_bytes)
    else:
        return "File {} does not exist.".format(filename)
```
command size digunakan untuk mendapatkan ukuran dari suatu file dengan bantuan library os kita dapat mendapatkan ukuran suatu file 

[reference images](assets/size.png)

6. command bye bye 

```sh
 elif command[0] == 'byebye':
            response = "Goodbye!"
            conn.sendall(response.encode('utf-8'))
            conn.close()
            break
```

bye bye akan langsung dihandel oleh sebuah fungsi bernama handle conn yang isi fungsi tersebut adalah untuk memeriksa setiap command, dan jika command adalah byebye maka conn.close() berarti mengakhiri hubungan antar socket

[reference images](assets/byebye.png)
[reference images](assets/byebyeout.png)

7. command connme 

```sh
elif command[0] == 'connme':
            response = "Connection established successfully."
            conn.sendall(response.encode('utf-8'))
            continue  
```
command connme berfungsi untuk memastikan apakah sebuah socket telah terhubung apa tidak 

[reference images](assets/connme.png)

# Program Server

1. Import Library 

```sh
import argparse
import os
import socket

```
-  import argparse: Mengimpor modul argparse yang digunakan untuk memproses argumen baris perintah.
   
- import os: Mengimpor modul os yang digunakan untuk berinteraksi dengan sistem operasi, seperti mengakses file dan direktori.

-  import socket: Mengimpor modul socket yang digunakan untuk membuat koneksi jaringan.

2. handle conn function 

```sh
def handle_client(conn):
    while True:
        data = conn.recv(1024).decode('utf-8')
        if not data:
            break

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
                response = upload(conn, filename)
                conn.sendall(response.encode('utf-8'))
            else:
                response = "Usage: upload [filename]"
            conn.sendall(response.encode('utf-8'))
            if response == "ready":
             continue 
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
            continue  
        else:
         response = "Invalid command."
         conn.sendall(response.encode('utf-8'))
```
sebuah fungsi untuk memeriksa sebuah command 
- yang bila ls, maka akan memanggil fungsi ls dan memberi daftar file 
- yang bila rm, maka akan memanggil fungsi rm dan menghapus file 
- yang bila upload, maka akan memanggil fungsi upload dan mengupload file baru 
- yang bila download, maka akan memanggil fungsi download dan membaca file dituju 
- yang bila size, maka akan memanggil fungsi size untuk mendapatkan ukuran suatu file 
- yang bila byebye maka akan memutuskan hubungan socket 
- yang bila connme maka akan mengirimkan pesan status jika socket aktif 

3. main 

```sh
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
            handle_client(conn)

if __name__ == "__main__":
    main()

```
dalam main kita akan menginisialisasikan sebuah host dan port, di mana sebuah socket TCP akan dibuat objeknya dan memanggil fungsi listen untuk mengakses koneksi dari client 
jika koneksi terus berjalan maka socket dan variabel alamat akan menyimpan fungsi accept 
dan di sinilah pengecekan command dipanggil 

# Program Client

1. library 

```
import socket
```

library yang dibutuhkan adalah socket, karena kita membutuhkan client yang akan dikoneksikan kepada server 

2. main 

```sh
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
```

dalam main, adanya inisialisasi host dan port ( harus sama dengan server agar dapat terkoneksi ) jangan lupa inisialisasi objek socket bertipe sock_stream (TCP) berarti antar server dan client memerlukan handshake, adapun tahapnya: 

- client_socket.sendall('connme'.encode('utf-8')): Ini bertujuan untuk memberi tahu server bahwa klien ingin membuka koneksi

- response = client_socket.recv(1024).decode('utf-8'): Menerima respons dari server setelah mengirim pesan 'connme' dan mendekodekannya dari byte ke string.

- print(response): Mencetak respons dari server

- while True:: Memulai loop tak terbatas untuk menerima dan mengirim perintah antara klien dan server. ( namun saat proses upload dia terganggu)

- command = input("Enter command: "): Memasukkan perintah.

-  client_socket.sendall(command.encode('utf-8')): Mengirim perintah yang dimasukkan pengguna ke server setelah mengonversi ke byte.

- if command == 'byebye':: jika command adalah byebye maka cetak 
print("Closing connection."): Mencetak pesan bahwa koneksi sedang ditutup dan 
break: Keluar dari loop jika pengguna memasukkan perintah 'byebye'.

- while "Continue" in response:: Memulai loop jika respons dari server mengandung kata "Continue"

# Tambahan 

pastikan antar client dan server sudah terhubung baik sehingga program dapat dijalankan

https://github.com/aefafifah/socket-programming-python/blob/main/assets/koneksi%20awal.png






