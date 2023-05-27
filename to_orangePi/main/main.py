import Robot
import socket

#IP = "0.0.0.0"
#IP = "172.17.0.1"
IP = "localhost"
PORT = 5005

tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
#time.sleep(2)
tcp_sock.bind((IP, PORT))
tcp_sock.listen(10)
#tcp_socket.listen(1)

doggo = Robot.Robot()

if __name__ == "__main__":
    conn, addr = tcp_sock.accept()
    conn.setblocking(0)
    doggo.fsm_process(conn)
