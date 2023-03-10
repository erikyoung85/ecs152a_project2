# Import socket module
from socket import *    

# Create a TCP server socket
#(AF_INET is used for IPv4 protocols)
#(SOCK_STREAM is used for TCP)

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

        hostname = message.split()[1].split(':')[0]
        port = int(message.split()[1].split(':')[-1].split("/")[0])

        serverSocket = socket(AF_INET, SOCK_STREAM)
        serverSocket.connect(('', port))

        request_uri = message.split()[1]
        filename = '/' + request_uri.split('/')[-1]
        processed_request = message.replace(request_uri, filename)

        serverSocket.send(processed_request.encode())

        responseMessage = serverSocket.recv(1024).decode()
        print(f"\nConnection to {hostname} sent message:")
        print(responseMessage)

        # Extract the status code from the response message
        statusCode = int(responseMessage.split()[1])

        if statusCode == 200:
            # Extract the content type from the response message
            contentType = responseMessage.split('Content-Type: ')[-1].split('\r\n')[0]

            # Send the response message to the client
            connectionSocket.send(responseMessage.encode())

            # Send a blank line to separate the headers from the body
            connectionSocket.send("\r\n".encode())

            if contentType.startswith('image'):
                # If the content is an image, read the data from the server socket
                imageData = serverSocket.recv(4096)
                while imageData:
                    # Forward the image data to the client
                    connectionSocket.send(imageData)
                    imageData = serverSocket.recv(4096)
            else:
                # If the content is not an image, read the data from the server socket
                responseData = responseMessage.encode()
                # responseLength = int(responseMessage.split('Content-Length: ')[-1].split('\r\n')[0])
                # while len(responseData) < responseLength:
                #     responseData += serverSocket.recv(4096)
                # Forward the response data to the client
                connectionSocket.send(responseData)
        else:
            # If the status code is not 200, forward the response message to the client
            connectionSocket.send(responseMessage.encode())

        # Close the server socket
        serverSocket.close()

    except IOError:
        # Send HTTP response message for file not found
        # Fill in start

        connectionSocket.send("HTTP/1.1 404 Not Found\r\nFile Not Found".encode())
        connectionSocket.send("\r\n".encode())

        # Fill in end

        # Close the client connection socket
        # Fill in start

        connectionSocket.close()

        # Fill in end

proxySocket.close()  

