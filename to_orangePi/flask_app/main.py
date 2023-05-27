from flask import Flask
from flask import render_template
from flask import request, json
import socket
import time

app = Flask(__name__)

#IP = "host-gateway"
#IP = "127.0.0.1"
IP = "localhost"
PORT = 5005

class fsm():
    def __init__(self):
        self.fsm = ["idle", "left", "right", "forward", "backward"]
        self.state_cur = 'idle'


@app.route('/')
def signUp():
    return render_template('main.html', state=fsm_obj.state_cur)


@app.route('/<state>', methods=['POST']) 
def doggo_sent_state(state):
    if state in fsm_obj.fsm:
        # try: 
            message = bytes(f'state: {state}', 'UTF-8')
            sock.sendto(message, (IP, PORT))
            try:
                sock.recv(1024).decode()
            except:
                sock.close()
                while sock.connect_ex((IP, PORT)) != 0:
                    time.sleep(1)
                    sock.__init__(socket.AF_INET, socket.SOCK_STREAM)
                sock.sendto(message, (IP, PORT))
        
            fsm_obj.state_cur = state
    
        # except BrokenPipeError:
        #     sock.close()
        #     sock.__init__(socket.AF_INET, socket.SOCK_STREAM)
        #     sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #     sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        #     while sock.connect_ex((IP, PORT)) != 0:
        #         print('sosi2')
        #         time.sleep(5)
        #     message = bytes(f'state: {state}', 'UTF-8')
        #     sock.sendto(message, (IP, PORT))
        #     fsm_obj.state_cur = state
        # except ConnectionResetError:
        #     while sock.connect_ex((IP, PORT)) != 0:
        #         sock.close()
        #         sock.__init__(socket.AF_INET, socket.SOCK_STREAM)
        #         sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #         sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        #         print('sosi3')
        #         time.sleep(5)
        #     message = bytes(f'state: {state}', 'UTF-8')
        #     sock.sendto(message, (IP, PORT))
        #     fsm_obj.state_cur = state
    return state


if __name__=="__main__":
    fsm_obj = fsm()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    test = 0
    while True:
        while sock.connect_ex((IP, PORT)) != 0:
            time.sleep(1)
            print('test1')
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('test2')
        #sock.sendall('send'.encode())
        #data = sock.recv(1024).decode()
        #if data == 'connection_established':
        app.run(host='0.0.0.0')
