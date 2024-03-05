import base64
import zlib
from io import BytesIO

from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes

def generate():
    new_key = RSA.generate(2048)
    private_key = new_key.exportKey()
    public_key = new_key.publickey().exportKey()

    with open('key.pri', 'wb') as f:
        f.write(private_key)

    with open('key.pub', 'wb') as f:
        f.write(public_key)

def get_rsa_cipher(keytype): # Pass this function the key type (pub or pri)
    with open(f'key.{keytype}') as f:
        key = f.read()
    rsakey = RSA.importKey(key)
    return (PKCS1_OAEP.new(rsakey), rsakey.size_in_bytes())

def encrypt(plaintext):
    compressed_text = zlib.compress(plaintext) # Pass in the plaintext and compress it.

    session_key = get_random_bytes(16) # Generate a random session key to be used in the AES cipher.
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(compressed_text) # Encrypt the compressed plaintext usering that cipher.

    cipher_rsa, _ = get_rsa_cipher('pub')
    encrypted_session_key = cipher_rsa.encrypt(session_key) # Add the sessions key and encrypt it with the RSA key.

    msg_payload = encrypted_session_key + cipher_aes.nonce + tag + ciphertext # All the info we need in one payload.
    encrypted = base64.encodebytes(msg_payload) # base64 encode it.
    retrun(encrypted)

def decrypt(encrypted):
    encrypted_bytes = BytesIO(base64.decodebytes(encrypted)) # First base64-decode the string into bytes.
    cipher_rsa, keysize_in_bytes = get_rsa_cipher('pri')

    encrypted_session_key = encrypted_bytes.read(keysize_in_bytes) # Read the encrypted session key and other params from encrypted byte string.
    nonce = encrypted_bytes.read(16)
    tag = encrypted_bytes.read(16)
    ciphertext = encrypted_bytes.read()

    session_key = cipher_rsa.decrypt(encrypted_session_key) # Decrypt the session key using the RSA private key.
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    decrypted = cipher_aes.decrypt_and_verify(ciphertext, tag) # Use the private key to to decrypt the message.

    plaintext = zlib.decompress(decrypted) # Decompress into plaintext byte string
    return plaintext

if __name__ == "__main__":
    plaintext = b'hey there you.'
    print(decrypt(encrypt(plaintext)))
    

