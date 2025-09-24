import os
def dir_test():
    folder_path = "logs"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"folder {folder_path} created.")
    else:
        print(f"folder {folder_path} already exists.")
