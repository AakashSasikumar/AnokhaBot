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
prevText = {}
prevReply = {}
people = []

"""
The request should be of the format- http://127.0.0.1:3126/?query=somestring&id=somenumber

"""


def startListening():
    global prevReply
    global prevText
    
    print("Listening")
    try:
        client, addr = serverSocket.accept()
        
    except KeyboardInterrupt:
        client.close()
        return
    except Exception as e:
        print("Could not establish connection with the client", e)
    finally:
        pass

    try:
        client.send(b'HTTP/1.1 200 OK' + CLRF)
        client.send(b'Content-Type: text/html' + CLRF*2)
        request = client.recv(1024)
        getRequest = request.splitlines()[0].decode("utf-8")[4:-9]
        query = urlsplit(getRequest).query
        parameters = parse_qs(query)
    except KeyboardInterrupt as e:
        print(e)
        return
    except Exception as e:
        print("Error while parsing the GET Request", e)
    finally:
        pass
    
    try:
        question = parameters["query"][0]
        chatID = parameters["id"][0]
        
    except KeyboardInterrupt as e:
        print(e)
        return
    except Exception as e:
        print("Error while parsing GET Request", e)
    finally:
        pass
    
    try:
        reply = Bot.response(question, chatID)
        print(prevText)

        if (question == "/wrong"):
            error = "id-" + chatID + "-txt-" + prevText[chatID] + "-rep-" + prevReply[chatID] + '\n'
            with open("SockErrors.txt", 'a') as file:
                file.write(error)
            return
        prevText[chatID] = question
        prevReply[chatID] = reply

    except Exception as e:
        print("Error while parsing GET Request", e)
        print("The value passed to the Bot was not defined")
    finally:
        pass
    
    try:
        print(reply)
        replyDict = {}
        if chatID not in people:
            reply = "Hello!  You seem to be a new face, allow me to introduce myself. I am anokhaBot I'm an \
                    artificial agent that can tell you anything about Anokha. I'm still learning a lot about \
                    anokha so it would be very helpful if you type /wrong whenever I go wrong somewhere and I promise to get better next time."
            people.append(chatID)
        if reply == "":
            reply = "I'm sorry, I didn't understand you. Could you rephrase it please?"
        replyDict["reply"] = reply
        replyDict = json.dumps(replyDict)
    except Exception as e:
        print("Error while parsing GET request", e)
    try:
        client.send(replyDict.encode())
    except KeyboardInterrupt as e:
        print(e)
        return
    except Exception as e:
        print("Could not send reply to client", e)
    finally:
        pass
    
    client.close()


while True:
    startListening()

serverSocket.close()
