from pydub import AudioSegment
import os

path = "D:/Coding Projects/lamejam41-eggcollector/assets/sounds/count/"
dbincrease = int(input("increase by "))

print(str(dbincrease))

def make_song_louder(name, db):
    song = AudioSegment.from_ogg(path + name)
    print(name)
    loudsong = song + db
    loudsong.export(path + name, format='ogg')

for f in os.listdir(path):
    make_song_louder(f, dbincrease)