import subprocess
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

def generate_keys():
    # Generate private key
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    # Generate the corresponding public key
    public_key = private_key.public_key()

    # Serialize private key to PEM format
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()  # No encryption for simplicity
    )

    # Serialize public key to PEM format
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Save the private and public keys to files
    with open("private_key.pem", "wb") as private_file:
        private_file.write(private_pem)

    with open("public_key.pem", "wb") as public_file:
        public_file.write(public_pem)

    # Example of signing data with the private key
    message = b"Important message"
    signature = private_key.sign(
        message,
        padding.PKCS1v15(),
        hashes.SHA256()
    )

    # Example of verifying the signature with the public key
    try:
        public_key.verify(
            signature,
            message,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        print("Signature is valid.")
    except Exception as e:
        print("Signature verification failed:", e)

    # Output the keys
    print("Private key:\n", private_pem.decode())
    print("Public key:\n", public_pem.decode())

def start_server():
    """Run the server script after generating keys."""
    subprocess.run(["python", "server.py"])

if __name__ == "__main__":
    # Step 1: Generate keys
    generate_keys()

    # Step 2: Start the server
    start_server()
