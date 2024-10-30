import os

path = input("Path to folder to subdelete (no / at the end) ")
extension = input("Extension (no .) ")

global kills
kills = 0

def parse_dir(dirpath):
    global kills
    files = os.listdir(dirpath)
    for file in files:
        if (os.path.isdir(dirpath + file)):
            parse_dir(dirpath + file + "/")
        elif file.endswith("." + extension):
            os.remove(dirpath + file)
            kills += 1

parse_dir(path + "/")
print(str(kills) + " has been killed lol")