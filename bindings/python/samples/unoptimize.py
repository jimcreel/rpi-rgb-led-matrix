import os
import json

def create_file_lists_by_directory(directory):
    file_lists_by_directory = {}
    
    for root, dirs, files in os.walk(directory):
        # Extract the current directory name from the root path
        current_directory_name = os.path.relpath(root, directory)
        # Replace backslashes with forward slashes for compatibility on Windows
        current_directory_name = current_directory_name.replace(os.path.sep, "/")
        
        # Initialize a list to store file names in the current directory
        file_list = []
        
        for file in files:
            # Add the file name to the list
            file_list.append(file)
        
        # Add the list of file names to the dictionary, using the directory name as the key
        file_lists_by_directory[current_directory_name] = file_list
    
    return file_lists_by_directory

if __name__ == "__main__":
    directory_path = "/home/jimcreel/code/rpi-rgb-led-matrix/bindings/python/samples/showdown"  # Replace with the path to your directory
    file_lists_by_directory = create_file_lists_by_directory(directory_path)

    # Save the file lists as a JSON file
    output_file = "file_lists.json"
    with open(output_file, "w") as json_file:
        json.dump(file_lists_by_directory, json_file, indent=4)

    print(f"File lists saved to {output_file}.")
