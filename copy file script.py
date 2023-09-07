import hashlib
import os
import shutil

# Function to calculate the hash of a file
def file_hash(filename):
    hash_obj = hashlib.sha256()
    with open(filename, "rb") as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            hash_obj.update(chunk)
    return hash_obj.hexdigest()

# Function to find and copy one original file for each duplicate in a directory
def copy_original_files(source_directory, destination_directory):
    # Dictionary to store file hashes
    file_hashes = {}

    # Iterate through all files and subdirectories in the source directory
    for root, dirs, files in os.walk(source_directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            file_info = (file_size, file_hash(file_path))

            # Check if the file info is already in the dictionary
            if file_info in file_hashes:
                # Copy the original file to the destination directory
                original_file_path = file_hashes[file_info]
                destination_path = os.path.join(destination_directory, os.path.basename(original_file_path))
                shutil.copy2(original_file_path, destination_path)
            else:
                file_hashes[file_info] = file_path

if __name__ == "__main__":
    source_directory = "C:\output"  # Replace with the source directory path
    destination_directory = "c:\output 2"
    # destination_directory = input("Enter the destination directory path: ")

    # Check if the source directory exists
    if not os.path.exists(source_directory):
        print("The source directory does not exist.")
    else:
        # Create the destination directory if it doesn't exist
        os.makedirs(destination_directory, exist_ok=True)

        # Copy one original file for each duplicate to the destination directory
        copy_original_files(source_directory, destination_directory)
