GRID_LENGTH = 10
GRID_HEIGHT = 10
map = {}

for x in range(GRID_LENGTH):
    for y in range(GRID_HEIGHT):
        map.update({(x, y): 0})

counter = 0
for row, heat in map.items():
    print(row, end = "")
    print(heat, end="  ")
    counter += 1
    if counter == 10:
        counter = 0
        print("\n")