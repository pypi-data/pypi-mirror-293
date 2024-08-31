import os


def create_path(path_or_file):
    path = os.path.dirname(path_or_file)
    if path and not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
        
        
if __name__ == '__main__':
    print(create_path("1/2"))
