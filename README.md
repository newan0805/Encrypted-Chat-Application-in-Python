
# Encrypted Chat Application

This is a simple encrypted chat application using RSA encryption for secure communication. The application involves three main components: the client, server, and key management system. The private and public keys are generated using RSA, and messages are encrypted before being sent and decrypted upon receipt.

### Features:
- RSA key generation for encryption and decryption
- Encrypted communication between the client and server
- Message integrity verification using digital signatures
- Simple command-line interface (CLI)

### File Structure:
```
├── client.py       # Client application to send and receive encrypted messages
├── server.py       # Server application to listen for client messages
├── main.py         # Key generation and server startup script
├── private_key.pem # Private key used for signing messages (generated automatically)
├── public_key.pem  # Public key used for verifying messages (generated automatically)
```

### Requirements:
- Python 3.7 or above
- `cryptography` library (for RSA encryption)

### Install Dependencies:
You can install the required dependencies by running the following command:
```bash
pip install cryptography
```

---

### Usage:

#### Step 1: Key Generation and Server Startup
1. **Run `main.py` to generate RSA keys and start the server.**
   - The `main.py` script will generate a private and public key, save them as `private_key.pem` and `public_key.pem`, respectively, and start the server.
   
   ```bash
   python main.py
   ```

   - The `server.py` script will then be launched automatically after the keys are generated. The server will listen for incoming encrypted messages from clients.

#### Step 2: Client Communication
1. **Run `client.py` to start the client application.**
   - The client will use the generated public and private keys to encrypt and decrypt messages.
   
   ```bash
   python client.py
   ```

2. **Enter your message in the client terminal.**
   - Type your message in the command prompt, and the message will be encrypted, sent to the server, and displayed after being decrypted.

---

### Key Concepts:

#### Key Generation:
- **Private Key** (`private_key.pem`): Used by the sender to sign messages and by the recipient to verify the integrity of the message.
- **Public Key** (`public_key.pem`): Used by the sender to encrypt messages and by the recipient to decrypt the messages.

#### Encryption and Decryption:
- **RSA Encryption**: RSA is an asymmetric cryptosystem where the public key is used for encryption and the private key for decryption.
- **Signature**: The message is signed with the private key before sending it, and the recipient verifies the signature using the public key to ensure the message has not been tampered with.

---

### Example Workflow:

1. **Start the server**:
   - Run `main.py` to generate the keys and start the server.
   ```bash
   python main.py
   ```

2. **Start the client**:
   - Run `client.py` to send a message to the server.
   ```bash
   python client.py
   ```

3. **Message sent and received**:
   - The client will encrypt the message using the public key, sign it using the private key, and send it to the server.
   - The server will decrypt the message using the private key and verify the signature using the public key.
   - The decrypted message will then be displayed on the client.

---

### Example Output:

1. **Server Output**:
   ```
   Server started...
   Waiting for a client to connect...
   Received: Hello, World!
   ```

2. **Client Output**:
   ```
   Enter your message: Hello, World!
   Message sent to server.
   ```

---

### Troubleshooting:
- Ensure that `cryptography` is installed correctly (`pip install cryptography`).
- If you encounter issues with connecting the client to the server, verify that both scripts (`client.py` and `server.py`) are using the correct keys.

---

### License:
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
