import os
from cryptor import decrypt

# Function to create a "decrypted" directory within the given directory.
def create_decrypted_directory(directory):
    decrypted_dir = os.path.join(directory, "decrypted") # Create the path for the "decrypted" directory.
    if not os.path.exists(decrypted_dir): # Check if the directory exists.
        os.mkdir(decrypted_dir) # Create the decrypted direcotry if it doesn't exist.

# Function to decrypt a file and save it in the "decrypted" directory.
def decrypt_and_save(input_directory, filename):
    decrypted_directory = os.path.join(input_directory, "decrypted") # Path to the "decrypted" dir.
    decrypted_filename = "decrypted_" + filename # Name of the decrypted file.

    # Check if a decrypted version of the file exists in the "decrypted" dir.
    if not os.path.exists(os.path.join(decrypted_directory, decrypted_filename)):
        # Read the contents of the file to decrypt.
        with open(os.path.join(input_directory, filename), 'rb') as f:
            contents = f.read()

        # Decrypt the contents
        decrypted_contents = decrypt(contents)

        # Write the decrypted contents to a new file in the "decrypted" directory.
        with open(os.path.join(decrypted_directory, decrypted_filename), 'wb') as f:
            f.write(decrypted_contents)

        # Print a message indicating the decryption and saving process.
        print(f"File '{filename} decrypted and saved as '{decrypted_filename}'.")

# Function to iterate over files in the input dir, decrypt them, and write them to the new dir.
def decrypted_files_in_directory(directory):
    create_decrypted_directory(directory) # Create the "decrypted" directory if it does not exist.

    # Iterate over all files in the input directory.
    for filename in os.listdir(directory):
        # Check if the item is a file and if it doesn't already start with "decrypted_"
        if os.path.isfile(os.path.join(directory, filename)) and not filename.startswith("decrypted_"):
            decrypt_and_save(directory, filename) # Decrypt and save the file.

if __name__ == '__main__':
    input_directory = input("Enter the directory path: ")
    decrypt_file_in_directory(input_directory)
