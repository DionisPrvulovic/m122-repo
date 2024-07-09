import os
import shutil

def clean_dump_folder():
    # Define the path to the 'dump' folder
    dump_path = os.path.join(os.getcwd(), 'dump')
    
    # Check if the 'dump' folder exists
    if os.path.exists(dump_path):
        # Loop through all the files and directories in the 'dump' folder
        for filename in os.listdir(dump_path):
            file_path = os.path.join(dump_path, filename)
            try:
                # If it is a file, delete it
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                # If it is a directory, delete it and all its contents
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                print(f"Deleted {file_path}")
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
    else:
        print("No 'dump' folder found in the current directory.")

if __name__ == "__main__":
    clean_dump_folder()
