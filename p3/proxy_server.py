import socket
import os 
import time

# Set the server IP address and port
# TODO Start
HOST, PORT = "127.0.0.1",9999
# TODO end

# Create a server socket, bind it to the specified IP and port, and start listening
# TODO Start
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((HOST, PORT))
serverSocket.listen(1)
debug_msg=0
if(debug_msg):
    print("[DEBUG]")
    print("[END DEBUG]")
    
    
# TODO end

while True:
    print('Ready to serve...')
    # Accept an incoming connection and get the client's address
    # TODO Start

    client_socket, client_address = serverSocket.accept()
    client_socket.settimeout(10)
    # TODO end

    print('Received a connection from:', client_address)

    try:
        # Receive request from the client
        # TODO Start
        try:
            request = client_socket.recv(1024).decode()
        except Exception as e:
            if(debug_msg):
                print("[DEBUG]")
                print(e)
                print("[END DEBUG]")
            continue
        # TODO end
        print(request)

        # Extract the filename from the request
        if request == "":
            request = "/ /"
        filename = request.split()[1].partition("/")[2]
        http_type = request.split()[2].partition("/")[0]
        file_path = "." + filename
        file_path = file_path.replace(":","/")
        file_level = file_path.rsplit("/",1)[0]
        if(os.path.exists(file_level)==0):
            os.makedirs(file_level,0o777)
        if(file_path=="." or file_path=="./"):
            continue
        if(debug_msg):
            print("[DEBUG]")
            print("++++++++++++++++++++++")
            print("filename  :"+filename)
            print("file_path :"+file_path)
            print("file_level:"+file_level) 
            print("++++++++++++++++++++++")
            print("[END DEBUG]")

        file_exist = "false"
        try:
            # Check whether the file exists in the cache
            with open(file_path, "r") as cache_file:
                output_data = cache_file.readlines()
            file_exist = "true"

            # ProxyServer finds a cache hit and generates a response message
            # Send the file data to the client
            client_socket.send("HTTP/1.1 200 OK\r\n".encode())
            client_socket.send("Content-Type:text/html\r\n\r\n".encode())
            # TODO Start
            for msg in output_data:
                client_socket.send(msg.encode())
            client_socket.close()
            
            # TODO End
            print('Read from cache')

        # Error handling if the file is not found in cache
        except FileNotFoundError:
            if file_exist == "false":
                # Create a socket on the proxy server
                # TODO Start
                proxy_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                proxy_server_socket.settimeout(10)
                # TODO End

                host_name = filename.replace("www.", "", 1)
                print("Host name is " + host_name)

                try:
                    print("Trying to connect to the web server")
                    # Connect the socket to the web server port
                    # TODO Start
                    proxy_connection_port = 80
                    if(http_type == "HTTP"):
                        proxy_connection_port=80
                    elif(http_type == "HTTPS"):
                        proxy_connection_port= 443
                    
                    addr = host_name.split("/")
                    
                    if(addr[1].find(":")):
                        proxy_connection_port=int(addr[1].split(":")[1])
                    if(debug_msg):
                        print("[DEBUG]")
                        print("addr      :",end="")
                        print(addr)
                        print("host_name :"+host_name)
                        print("port      :"+str(proxy_connection_port))
                        print("[END DEBUG]")
                    www_addr = addr[1].split(":")[0]
                    proxy_server_socket.connect((www_addr,proxy_connection_port))
                    
                    # TODO End
                    print("Connected successfully")

                    # Create a temporary file on this socket
                    # Create the HTTP GET request message to fetch the file from the web server
                    # Write the request to the file-like object
                    file_obj = proxy_server_socket.makefile('rw', None)
                    server_file_path = "/"+filename.partition('/')[2].partition('/')[2]
                    request_message = f"GET {server_file_path} HTTP/1.1\r\n"
                    # print(request_message)
                    # file_obj.write(request_message)  # Write the request to the file-like object
                    # file_obj.flush()
                    # file_obj.close()
                    proxy_server_socket.send(request_message.encode())
                    print("Sent the request to the web server successfully")

                    # Read the response into buffer
                    # TODO Start
                    
                    # time.sleep(0.2)
                    if(debug_msg):
                        print("[DEBUG]")
                        print("================================================")
                    web_message = ""
                    while True:
                        print("Connecting")
                        data = proxy_server_socket.recv(1024).decode()
                        web_message += data
                        if not data:
                            break
                    if(debug_msg):
                        print(web_message)
                    
                    # TODO End
                    print("received the request to the web server successfully")
                    if(debug_msg):
                        print("================================================")
                        print("[END DEBUG]")
                    print("Read the file from the web server successfully")

                    # Create a new file in the cache for the requested file
                    # TODO Start
                    state_code_response = web_message.split(" ")[1]
                    web_message = web_message.partition("\n")[2].partition("\n")[2]
                    if(debug_msg):
                        print("[DEBUG]")
                        print("state  :",end="")
                        print(state_code_response)
                        print("message:")
                        print(web_message)
                        print("[END DEBUG]")
                    if(state_code_response=="200"):
                        with open(file_path, "w") as cache_file:
                            cache_file.write(web_message)
                            cache_file.flush()
                            cache_file.close()
                    elif(state_code_response=="404"):
                        pass
                    # TODO End
                    print("Wrote the file to the cache successfully")

                    # Send the response to the client socket
                    # TODO Start
                    if(state_code_response == "200"):
                        if (http_type == "HTTP"):
                            client_socket.send("HTTP/1.1 200 OK\r\n".encode())
                            client_socket.send("Content-Type:text/html\r\n\r\n".encode())
                            client_socket.send(web_message.encode())
                        elif (http_type == "HTTPS"):
                            pass                          
                    elif(state_code_response == "404"):
                        if(http_type == "HTTP"):
                            client_socket.send("HTTP/1.1 404 Not Found\r\n".encode())
                            client_socket.send("Content-Type:text/html\r\n\r\n".encode())
                            client_socket.send(web_message.encode())
                        elif (http_type == "HTTPS"):
                            pass
                    if(debug_msg):
                        print("[DEBUG]")
                        print(http_type+state_code_response)
                        print("[END DEBUG]")
                    # TODO End
                    print("Sent the data from the web server to the client")
                except Exception as e:
                    print("Illegal request")
                    if(debug_msg):
                        print("[DEBUG]")
                        print(e)
                        print("[END DEBUG]")
            else:
                pass
                # HTTP response message for file not found
                # TODO Start
                # TODO End

    finally:
        # Close the client socket
        client_socket.close()

# Close the server socket
serverSocket.close()
