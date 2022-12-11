import socket
import os
from dotenv import load_dotenv
from time import ctime,time

sibar=time()
print(sibar)
STX=b'\x02'
TYPE_A=b'\x5A' #수위
TYPE_B=b'\x5B' #조도
TYPE_C=b'\x5C' #출입
ETX=b'\0x03'
load_dotenv()
host=os.environ.get('host')
port=int(os.environ.get('port'))
ip=[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
print(ip)


ip=[(chr(int(i))) for i in (ip.split('.'))]

def run_client(Type,Data):

    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
        sock.connect((host, port))

        print(Data)
        print(STX+TYPE_A+''.join(ip).encode()+str(Data).encode()+'\n'.encode())
        sock.sendall(STX+TYPE_A+''.join(ip).encode()+'\n'.encode())
            
        # recive=sock.recv(1024)
                
            
        # print(recive.decode(),"recive")
       
        sock.close()
            
if __name__ == "__main__":
    run_client(TYPE_A,123)
    