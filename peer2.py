import socket
import sqlite3
import datetime

dbCon = sqlite3.connect('databaseDB')
cursor = dbCon.cursor()

msgTable = ''' CREATE TABLE IF NOT EXISTS databaseTable(msgID INTEGER PRIMARY KEY, message TEXT NOT NULL, host TEXT NOT NULL, time_sent TEXT NOT NULL);'''
cursor.execute(msgTable)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
hostname = socket.gethostname()
host = socket.gethostbyname(hostname)
port = 3001

sock.bind((host, port))
while True:
    print("Read to receive data: ")
    time_sent = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data, addressInfo = sock.recvfrom(1024)
    print(data.decode("utf-8") +" "+ "from" + str(addressInfo), time_sent)
     
    print("Ready to send data: ")
    message = input("Write your message: ").encode("utf-8")
    sock.sendto(message, (host, 3000))
    print(f"{message}, {(host, port)}, {time_sent}",)
    
    msgData = data.decode("utf-8")
    msgData = message
    hostData = str(addressInfo)
    
    cursor.execute("INSERT INTO databaseTable(message, host, time_sent) VALUES (?,?,?)", (msgData, hostData, time_sent))
    dbCon.commit()
    
    selectQuery = ''' SELECT * FROM databaseTable'''
    cursor.execute(selectQuery)
    selectedMessage = cursor.fetchall()
    print(selectedMessage)