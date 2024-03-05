import os
from cryptor import decrypt

def decrypt_file(file_path):
    if not os.path.exists(file_path):
        print('File not found.')
        return

    # Extract filename from the provided path.
    file_name = os.path.basename(file_path)

    # Prepend "decrypted_" to the filename.
    decrypted_filename = "decrypted_" + filename

    with open(file_path, 'rb') as f:
        contents = f.read()

    decrypted_contents = decrypt(contents)

    with open(decrypt_filename, 'wb') as f:
        f.write(decrypted_contents)

    print(f'File decrypted successfully. Decrypted file saved as: {decrypted_filename}")

if __name__ == '__main__':
    file_path = input("Enter the path of the file to decrypt: ")
    decrypt_file(file_path)

