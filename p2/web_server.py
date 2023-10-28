import socket
import sys

# Server setup
# Specify the IP address and port number (Use "127.0.0.1" for localhost on local machine)
# TODO Start
# HOST, PORT = "127.0.0.1",10045
HOST, PORT = "127.0.0.1",10046

# TODO end


# 1. Create a socket
# 2. Bind the socket to the address
# TODO Start
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# TODO End

# Listen for incoming connections (maximum of 1 connection in the queue)
# TODO Start

serverSocket.bind((HOST,PORT))
serverSocket.listen(1)
# TODO End

# Start an infinite loop to handle incoming client requests
while True:
    print('Ready to serve...')

    # Accept an incoming connection and get the client's address
    # TODO Start
    connectionSocket, address = serverSocket.accept()
    connectionSocket.settimeout(10)
    # TODO End
    print(str(address) + " connected")

    try:
        # Receive and decode the client's request
        # TODO Start
        message = connectionSocket.recv(1024).decode()
        print("MESSAGE:")
        print(message)
        print("")
        # TODO End

        # If the message is empty, set it to a default value
        if message == "":
            message = "/ /"
            filename = ""
        else:
        # Print the client's request message
            print(f"client's request message: \n {message}")

            # Extract the filename from the client's request
            # TODO Start
            message_arr_1 = message.split(" ")
            
            if message_arr_1[0] == "GET":
                message_arr = message_arr_1[1].split("/")
                filename = "."+message_arr_1[1]
                # print(message_arr)
                if(message_arr[1]=="index.html"):  # or message_arr[1]=="/index" or message_arr[1]==""):
                    filename = "index.html"
                elif(message_arr[1]==""):
                    connectionSocket.send("HTTP/1.1 404 Not Found\n\n<h1>404 Not Found</h1>".encode())
                    connectionSocket.close()
                    continue
                elif(message_arr[1]=="test"):
                    raise NameError(message_arr[2])
                else:
                    # filename = ""
                    pass
            else:
                pass
        # TODO End
        print(f"Extract the filename: {filename}")

        # Open the requested file
        # Read the file's content and store it in a list of lines
        f = open(filename)
        outputdata = f.readlines()
        # 1. Send an HTTP response header to the client
        # 2. Send the content of the requested file to the client line by line
        # 3. Close the connection to the client
        # TODO Start
        connectionSocket.send(("HTTP/1.1 200 OK\n\n").encode())
        http_inside = ""
        for msg in outputdata:
            # http_inside+=msg
            connectionSocket.sendall((msg).encode())
        # print(http_inside)
        # connectionSocket.sendall(http_inside.encode())
        connectionSocket.close()
        f.close()
        # TODO End

    except NameError as e:
        # If the requested file is not found, send a 404 Not Found response
        # TODO Start
        
        Errorargs= e.args
        # print(type(Errorargs))
        print((Errorargs))
        
        arg=Errorargs[0]
        print(f"in NameError: {arg}")
        if(arg=="404"):
            connectionSocket.send("HTTP/1.1 404 Not Found\n\n<h1>404 Not Found</h1>".encode())
            connectionSocket.close()
        else:
            print(f"in Error: {arg}")
            connectionSocket.send(f"HTTP/1.1 {arg}\n\n".encode())
            connectionSocket.send(f"<h1>Get Error Code(Testing): {arg}</h1>".encode())
        connectionSocket.close()
            
        pass
    except (OSError) as e:
        connectionSocket.send("HTTP/1.1 404 Not Found\n\n<h1>404 Not Found</h1>".encode())
        connectionSocket.close()
    except Exception as e:
        connectionSocket.close()
        print("Exception:")
        print(e)
        # TODO End
    
serverSocket.close()
