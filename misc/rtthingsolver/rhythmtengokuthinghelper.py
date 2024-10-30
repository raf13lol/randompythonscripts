shittocalc = []
shittocalcbase = []
basekey = int(input("what's the base key of the bank? "))

recentestinput = input("number of note? or just put 'd' if done ")

while recentestinput != "d":
    if not (int(recentestinput) - basekey) in shittocalc:
        shittocalc.append(int(recentestinput) - basekey)
        shittocalcbase.append(int(recentestinput))
    recentestinput = input("number of note? or just put 'd' if done ")

shittocalc.sort()
shittocalcbase.sort()

print("done, " + str(shittocalc))
print("base, " + str(shittocalcbase))