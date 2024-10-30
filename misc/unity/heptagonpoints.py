

points = [
            [255.5, 0  ],
            [461  , 102],
            [511  , 328],
            [369  , 511],
            [142  , 511],
            [0    , 328],
            [51   , 101]
         ]

scale = 0.985

def calcPoint(index):
    global points
    global scale
    point = points[index]

    print(f"Point {index}: X= {(point[0]-255.5) / 255.5 / 2 * scale}  -  Y=  {(point[1]-255.5) / 255.5 / 2 * scale * -1}  ")

for i in range(len(points)):
    calcPoint(i)