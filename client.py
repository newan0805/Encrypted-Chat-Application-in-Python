import socket
import threading
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from datetime import datetime
import os

# Load the client's private and public keys
with open("private_key.pem", "rb") as private_file:
    private_key = serialization.load_pem_private_key(private_file.read(), password=None)

with open("public_key.pem", "rb") as public_file:
    public_key = serialization.load_pem_public_key(public_file.read())

# Function to receive and decrypt messages
def receive_messages(client_socket):
    while True:
        try:
            # Receive encrypted message
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

            # Add to conversation history
            conversation_history.append(f"Server: {decrypted_message.decode()}")
            print_conversation_history()

        except Exception as e:
            print(f"Error receiving message: {e}")
            break

# Function to print the conversation history
def print_conversation_history():
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear console for a fresh view
    print("---- Conversation History ----")
    for msg in conversation_history:
        print(msg)
    print("\nEnter your message: ", end="")

# Set up client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 12345))

# Prompt user for a show name (username)
show_name = input("Enter your show name: ")

# List to store the conversation history
conversation_history = []

# Start a thread to receive messages
receive_thread = threading.Thread(target=receive_messages, args=(client,))
receive_thread.daemon = True  # This ensures the thread will exit when the main program ends
receive_thread.start()

# Send messages to the server
while True:
    message = input("Enter your message: ")

    if message.lower() == 'exit':  # Graceful exit if user types 'exit'
        client.send(b"Goodbye!")
        client.close()
        break

    if message:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Add to conversation history with timestamp and show name
        conversation_history.append(f"[{timestamp}] {show_name}: {message}")
        print_conversation_history()

        # Encrypt the message
        encrypted_message = public_key.encrypt(
            message.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        try:
            # Send the encrypted message
            client.send(encrypted_message)
        except Exception as e:
            print(f"Error sending message: {e}")
            break
