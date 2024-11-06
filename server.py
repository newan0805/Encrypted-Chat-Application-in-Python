import socket
import threading
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

# Load the server's private and public keys
with open("private_key.pem", "rb") as private_file:
    private_key = serialization.load_pem_private_key(private_file.read(), password=None)

with open("public_key.pem", "rb") as public_file:
    public_key = serialization.load_pem_public_key(public_file.read())

# List of connected clients
clients = []

# Function to broadcast messages to all clients
def broadcast(message, sender_client):
    for client in clients:
        if client != sender_client:
            client.send(message)

# Function to handle individual clients
def handle_client(client_socket):
    while True:
        try:
            # Receive encrypted message from client
            message = client_socket.recv(1024)
            if not message:
                break

            # Decrypt the message
            decrypted_message = private_key.decrypt(
                message,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            print(f"Received: {decrypted_message.decode()}")

            # Broadcast the decrypted message to all clients
            broadcast(message, client_socket)

        except Exception as e:
            print(f"Error: {e}")
            break

    # Remove the client from the list and close the connection
    clients.remove(client_socket)
    client_socket.close()

# Set up server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 12345))
server.listen(5)

print("Server started, waiting for clients to connect...")

# Accept incoming connections and start a new thread for each client
while True:
    client_socket, client_address = server.accept()
    print(f"Client {client_address} connected.")

    # Add the client to the list
    clients.append(client_socket)

    # Start a new thread to handle the client
    thread = threading.Thread(target=handle_client, args=(client_socket,))
    thread.start()
