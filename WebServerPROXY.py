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

        #process request to forward
        request_uri = message.split()[1]
        filename = '/' + request_uri.split('/')[-1]
        processed_request = message.replace(request_uri, filename)

        #forward request
        serverSocket.send(processed_request.encode())

        responseMessage = serverSocket.recv(1024).decode()
        print(f"\nConnection to {hostname} sent message:")
        print(responseMessage)

        # Extract the status code from the response message
        statusCode = int(responseMessage.split()[1])

        if statusCode == 200:
            responseData = responseMessage.encode()
            connectionSocket.send(responseData)
        else:
            # If the status code is not 200, forward the response message to the client
            connectionSocket.send(responseMessage.encode())

        connectionSocket.close()
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

