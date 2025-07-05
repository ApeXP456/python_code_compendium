import socket

target_host = "0.0.0.0"
target_port = 9998

# Create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the target host and port
client.connect((target_host, target_port))

# Send some data
client.send(b"GET / HTTP/1.1\r\nHost: 0.0.0.0\r\n\r\n")

# Receive some data
response = client.recv(4096)

# Print the response
print(response.decode())

# Close the connection
client.close()
