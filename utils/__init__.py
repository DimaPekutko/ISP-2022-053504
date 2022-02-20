def error_exit(desc: str):
    print(f"Error: {desc}")
    exit()

def get_file_ext(path: str):
    ext = str(path).split(".")
    return ext[len(ext)-1]