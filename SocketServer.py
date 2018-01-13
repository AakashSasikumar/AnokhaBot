import socket
from urllib.parse import urlsplit, parse_qs
import Bot
import json

host = ''
port = 3126
CLRF = b'\r\n'


serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((host, port))
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.listen(5)

while True:
    print("Listening")
    try:
        client, addr = serverSocket.accept()
        
    except KeyboardInterrupt:
        client.close()
        break
    except Exception as e:
        print("Could not establish connection with the client", e)
    finally:
        pass

    try:
        client.send(b'HTTP/1.1 400 BAD Request' + CLRF)
        client.send(b'Content-Type: text/html' + CLRF*2)
        request = client.recv(1024)
        getRequest = request.splitlines()[0].decode("utf-8")[4:-9]
        query = urlsplit(getRequest).query
        parameters = parse_qs(query)
    except KeyboardInterrupt as e:
        print(e)
        break
    except Exception as e:
        print("Error while parsing the GET Request", e)
    finally:
        pass
    
    try:
        question = parameters["query"][0]
        
    except KeyboardInterrupt as e:
        print(e)
        break
    except Exception as e:
        print("Error while parsing GET Request", e)
    finally:
        pass
    
    try:
        reply = Bot.response(question)
        
    except Exception as e:
        print("Error while parsing GET Request", e)
        print("The value passed to the Bot was not defined")
    finally:
        pass
    replyDict = {}
    replyDict["reply"] = reply
    replyDict = json.dumps(replyDict)
    try:
        client.send(replyDict.encode())
    except KeyboardInterrupt as e:
        print(e)
        break
    except Exception as e:
        print("Could not send reply to client", e)
    finally:
        pass
    
    client.close()

serverSocket.close()
