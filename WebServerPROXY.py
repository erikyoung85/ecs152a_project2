# Import socket module
from socket import *    

# Create a TCP server socket
#(AF_INET is used for IPv4 protocols)
#(SOCK_STREAM is used for TCP)

cache = {}

proxySocket = socket(AF_INET, SOCK_STREAM)

# Fill in start

proxySocket.bind(('', 8888))
proxySocket.listen(1)

# Fill in end 

# Server should be up and running and listening to the incoming connections
while True:
    print('Ready to serve...')

    # Set up a new connection from the client
    connectionSocket, addr = proxySocket.accept() #Fill in start             #Fill in end

    # If an exception occurs during the execution of try clause
    # the rest of the clause is skipped
    # If the exception type matches the word after except
    # the except clause is executed 
    try:
        # Receives the request message from the client
        message = connectionSocket.recv(1024).decode()  #Fill in start           #Fill in end
        print(f"\nconnection at {addr} sent message:")
        print(message)

        response = b""

        # if in cache
        reqLine = message.split('\n')[0]
        if reqLine in cache:
            print("getting response from cache")
            response = cache[reqLine]

        # if not in cache
        else:
            #process request to forward
            request_uri = message.split()[1]

            request_uri_list = request_uri.split('/')
            # grab target server host and port
            targetServer = request_uri_list[1]
            # delete proxy host and port
            del request_uri_list[1]
            # make new uri for target server
            new_uri = '/'.join(request_uri_list)
            if new_uri == '':
                new_uri = '/'

            # change request line
            processed_request = message.replace(request_uri, new_uri)

            # change host line
            currHost = message.split('\n')[1].split()[1]
            processed_request = processed_request.replace(currHost, targetServer)

            # get hostname and port from serverDetails
            targetServer = targetServer.split(':')
            hostname = targetServer[0]
            port = int(targetServer[1]) if len(targetServer) > 1 else 80
            print(f"forwarding to {hostname}:{port}\n")

            #forward request
            serverSocket = socket(AF_INET, SOCK_STREAM)
            serverSocket.connect((hostname, port))
            serverSocket.sendall(processed_request.encode())

            # get message from server and send to client
            chunkNum = 1
            while True:
                chunk = serverSocket.recv(4096)
                if len(chunk) == 0:     # No more data received, quitting
                    break
                response += chunk
                print(f"sent {chunkNum} chunks")
                chunkNum += 1

            # add to cache
            cache[reqLine] = response

        # send response to client
        connectionSocket.sendall(response)

        serverSocket.close()
        connectionSocket.close()

    except IOError:
        # Send HTTP response message for file not found
        # Fill in start

        print("\nerror occurred\n")
        connectionSocket.sendall("HTTP/1.1 404 Not Found\r\nFile Not Found".encode())
        connectionSocket.sendall("\r\n".encode())

        # Fill in end

        # Close the client connection socket
        # Fill in start

        connectionSocket.close()

        # Fill in end

proxySocket.close()  

