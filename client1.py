import socket
import struct
import json

phone=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

phone.connect(('127.0.0.1',8081))

while 1:
    msg=input('--')
    if not msg:continue
    phone.send(msg.encode('utf-8'))



    #1.收报头
    header=phone.recv(4)
    total_size=struct.unpack('i',header)[0]

    header_bytes=phone.recv(total_size)
    header_json=header_bytes.decode('utf-8')
    header_dic=json.loads(header_json)
    total_size=header_dic['total_size']
    #2.从报头解析数据

    recv_size = 0
    recv_data=b''
    while recv_size < total_size:
        data=phone.recv(1024)
        recv_data+=data
        recv_size+=len(data)
    print(recv_data.decode('GBK'))

phone.close()