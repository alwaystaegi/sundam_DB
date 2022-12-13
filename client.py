# 댐 관리 프로젝트(?)의 클라이언트용 


import socket
import os
from dotenv import load_dotenv
import time
import datetime

#변화 없는 값들 STX=시작
STX=b'\x02' # Start of Text
WATER_LEVEL=b'\x5A' #수위 보기 쉽게 바꾸면 될듯
LIGHT=b'\x5B' #조도
WORK_NMPR=b'\x5C' #출입
ETX=b'\x03'# End of Text


load_dotenv() #환경변수 불러오기(호스트 주소를 불러오기 위함... 호스트주소IP:효택's LG노트북)
host=os.environ.get('host')
port=int(os.environ.get('port'))

# 현재 사용중인 PC(여기선 라즈베리파이)의 IP가져오기
ip=[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
ip=[i for i in (ip.split('.'))]
def get_damid():
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        sock.sendall(b'\x02'+b'\x01'+b'\x03')
        recv=sock.recv(1024)
        print(int(recv[2]))
        sock.close()
        return recv[2]

def checkDB(Type):
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        
        sock.sendall(b'\x02'+b'\x02'+chr(int(Type)).encode()+b'\x03')
        print(chr(int(Type)).encode())
        sock.recv(1024)
        sock.close()

def run_client(Type,Data):
    checkDB(Type/10)
    



    """
    Type: 1의 자리: 데이터 종류 
    10의 자리부터: 댐 번호
    """
    #측정 시간
    now=datetime.datetime.now()
    year=str(now.year).rjust(4,'0')
    month=str(now.month).rjust(2,'0')
    day=str(now.day).rjust(2,'0')
    hour=str(now.hour).rjust(2,'0')
    minute=str(now.minute).rjust(2,'0')
    second=str(now.second).rjust(2,'0')
    
    #서버와 소켓통신
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
        sock.connect((host, port))


        #일단 ip주소를 인코딩 할 방법을 생각한 후 아래의 코드를 사용할 예정-> 
        #현재 문제점: 1.문자로 인코딩하면 자바에서 ip주소가 3자리인지 2자리인지 구분 불가 
        #             2.숫자로 인코딩하면 가끔 ip값중 10이 있다면 자바에서 end of line으로 취급해서 그 다음을 안읽음
        # message=STX+TYPE_A+''.join(ip).encode()+year.encode()+month.encode()+day.encode()+hour.encode()+minute.encode()+second.encode()
        message=STX+chr(Type).encode()
        print(chr(Type).encode())
        length=None
        ipEncode= None
        for i in ip:
            if length==None:
                length=str(len(str(i))).encode()
                ipEncode=str(i).encode()
            else :    
                length= length+str(len(str(i))).encode()
                ipEncode= ipEncode+str(i).encode()
        timemessage=year.encode()+month.encode()+day.encode()+hour.encode()+minute.encode()+second.encode()
        datamessage=str(len(str(Data))).encode()+str(Data).encode()
        print(year.encode())
        message=message=message+timemessage+datamessage+ETX+'\n'.encode()   


        print("보낸 메시지"+message.decode())


        #메시지를 서버에 보냄.
        sock.sendall(message)
            
        #아직 리시브 메시지를 구현안함... 구현하면 주석제거    
        # recive=sock.recv(1024)
                

        # print(recive.decode(),"recive")
        
        sock.close()
# run_client(13,12)