import socket
import os
import subprocess
import struct
import json

phone=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
phone.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

phone.bind(('127.0.0.1',8081))

phone.listen(5)

while True:
    conn,client_addr=phone.accept()

    while True:
        try:
            data=conn.recv(1024)
            if not data:break
            print('客户端的数据为',data)
            # 1、conn.send(data.upper())
            obj=subprocess.Popen(data.decode('utf-8'),shell=True,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            stdout=obj.stdout.read()
            stderr=obj.stderr.read()
            #1、数据长度转固定长度报头
            header_dic={
                'folename':'a.txt',
                'md5':'graga',
                'total_size':len(stdout) + len(stderr)
            }
            header_json=json.dumps(header_dic)
            header_bytes=header_json.encode('utf-8')

            header_len=struct.pack('i',len(header_bytes))
            #2、把报头发送给客户端
            conn.send(header_len)
            conn.send(header_bytes)
            #3、发送数据
            conn.send(stdout)
            conn.send(stderr)
        except ConnectionResetError:
            break

    conn.close()

phone.close()

