import os

path = input("Path to folder to subreplace (no / at the end) ")
extension = input("Extension (no .) ")
replaceto = input("Extension replace (no .) ")

global kills
kills = 0

def parse_dir(dirpath):
    global kills
    files = os.listdir(dirpath)
    for file in files:
        if (os.path.isdir(dirpath + file)):
            parse_dir(dirpath + file + "/")
        elif file.endswith("." + extension):
            os.rename(dirpath + file, dirpath + file[0:file.rfind(".")] + "." + replaceto)
            kills += 1

parse_dir(path + "/")
print(str(kills) + " has been reaaplced lol")