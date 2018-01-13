import socket
from urllib.parse import urlsplit, parse_qs
import Bot

host = ''
port = 8081
CLRF = b'\r\n'


serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((host, port))
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.listen(5)
while True:
    client, addr = serverSocket.accept()
    request = client.recv(1024)
    getRequest = request.splitlines()[0].decode("utf-8")[4:-9]
    getRequest = getRequest
    query = urlsplit(getRequest).query
    parameters = parse_qs(query)
    question = parameters["query"][0]
    reply = Bot.response(question)
    replyDict = {}
    replyDict["reply"] = reply
    replyDict = str(replyDict)
    client.send(replyDict.encode())
    client.close()

serverSocket.close()
