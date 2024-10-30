import requests, math, os

def url(arg):
    return f"https://example.com/{arg}"

def arggeneration(index):
    letters = "abcdefghijklmnopqrstuvwxyz"
    return [letters[math.floor(index / 26)] + letters[index % 26], index == 700]

path = os.path.dirname(__file__) + "/serverprober/"

i = 0
while True:
    arg = arggeneration(i)
    i += 1
    u = url(arg[0])
    r = requests.get(u)
    if r.status_code == 200:
        f = 0 
        if os.path.exists(path + u[u.rfind("/"):len(u)]):
            f = open(path + u[u.rfind("/"):len(u)], "w")
        else:
            f = open(path + u[u.rfind("/"):len(u)], "x")
        f.write(r.text)
        print(u)
        print(path + u[u.rfind("/"):len(u)])
        f.close()
    if arg[1]:
        break

print("done")