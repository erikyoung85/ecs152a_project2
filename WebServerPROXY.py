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
        serverSocket.connect((hostname, port))

        serverSocket.send(message.encode())
        
        responseMessage = serverSocket.recv(1024).decode()

        # Extract the path of the requested object from the message
        # The path is the second part of HTTP header, identified by [1]
        filename = responseMessage.split()[1]

        # Because the extracted path of the HTTP request includes 
        # a character '\', we read the path from the second character 
        f = open(filename[1:], 'rb')

        # Store the entire contenet of the requested file in a temporary buffer
        outputdata = f.read() #Fill in start         #Fill in end

        # Send the HTTP response header line to the connection socket
        # Fill in start
        connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
        if '.jpg' in filename:
            connectionSocket.send("Content-Type: image/jpeg\r\n".encode())

        # required blank line
        connectionSocket.send("\r\n".encode())
        
        # Fill in end

        # Send the content of the requested file to the connection socket
        connectionSocket.send(outputdata)
        # for i in range(0, len(outputdata)):  
        #     connectionSocket.send(outputdata[i].encode())

        connectionSocket.send("\r\n".encode())
        
        # Close the client connection socket
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
