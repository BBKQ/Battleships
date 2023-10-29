"""BATTLESHIP DESTROYER"""
 
from print_enchancer import *
from ships import Ship
import random
 
GRID_LENGTH = 10
GRID_HEIGHT = 10
X_COORDINATES = "ABCDEFGHIJ"
Y_COORDINATES = "0123456789"

mode = "easy"
game_over = False

player_next_grid = []
player_occupied_spaces = []
player_sunken_spaces = []
player_shots_fired = []
opponent_next_grid = []
opponent_occupied_spaces = []
opponent_sunken_spaces = []
opponent_shots_fired = []
 
player_destroyer         = Ship("Destroyer", 2, "player")
player_cruiser           = Ship("Cruiser", 3, "player")
player_submarine         = Ship("Submarine", 3, "player")
player_battleship        = Ship("Battleship", 4, "player")
player_aircraftCarrier   = Ship("Aircraft Carrier", 5, "player")
opponent_destroyer       = Ship("Destroyer", 2, "opponent")
opponent_cruiser         = Ship("Cruiser", 3, "opponent")
opponent_submarine       = Ship("Submarine", 3, "opponent")
opponent_battleship      = Ship("Battleship", 4, "opponent")
opponent_aircraftCarrier = Ship("Aircraft Carrier", 5, "opponent")
 
player_ships = [player_destroyer, 
                player_cruiser, 
                player_submarine, 
                player_battleship, 
                player_aircraftCarrier]
 
opponent_ships = [opponent_destroyer,
                  opponent_cruiser,
                  opponent_submarine,
                  opponent_battleship, 
                  opponent_aircraftCarrier]
 
def square_validator():
    while True:
        move = input()
        if len(move) != 2:
            slow_print("This is not a valid square. Try again.")
        elif move.upper()[0] in X_COORDINATES and move[1] in Y_COORDINATES:
            x, y = X_COORDINATES.find(move[0].upper()), int(move[1])
            return x, y
        else:
            slow_print("This is not a valid square. Try again.")

def player_ship_placement(ship_list):
    for ship in ship_list:
        xA, yA, xB, yB, is_horizontal = ship_placement_validator(ship)
        ship.pointA = [xA, yA]
        ship.pointB = [xB, yB]
        ship.is_horizontal = is_horizontal
        update_grid(player_next_grid, player_occupied_spaces, player_sunken_spaces, player_shots_fired)
 
def ship_placement_validator(ship):    
    slow_print("\n{} is {} spaces big.".format(ship.name, ship.size))
    while True:
        slow_print("\nWhere do you want it to start?")
        xA, yA = square_validator()
        slow_print("\nWhere do you want it to end?")
        xB, yB = square_validator() 
 
        if xA == xB and yA != yB:
            if abs(yA - yB) == ship.size - 1:
                is_horizontal = False
                add_ship_coordinates(xA, yA, xB, yB, is_horizontal, player_occupied_spaces)
                slow_print(f"{ship.name}'s coordinates are {X_COORDINATES[xA]+str(yA), X_COORDINATES[xB]+str(yB)}")
                return xA, yA, xB, yB, is_horizontal
            else:
                slow_print("{} can't be placed that way. Remember, it is {} spaces big.".format(ship.name, ship.size))               
        elif yA == yB and xA != xB:
            if abs(xA - xB) == ship.size - 1:
                is_horizontal = True
                add_ship_coordinates(xA, yA, xB, yB, is_horizontal, player_occupied_spaces)
                slow_print(f"{ship.name}'s coordinates are {X_COORDINATES[xA]+str(yA), X_COORDINATES[xB]+str(yB)}")
                return xA, yA, xB, yB, is_horizontal              
            else:
                slow_print("{} can't be placed that way. Remember, it is {} spaces big.".format(ship.name, ship.size))          
        else:
            fast_print("""This is not a valid position for a ship.
Remember that the ships can only be placed vertically or horizontally (not diagonally).
Please enter valid ship positioning.""")
 
def add_ship_coordinates(xA, yA, xB, yB, is_horizontal, occupied_spaces):
    spaces = []
    if is_horizontal:
        if xA > xB:
            xA, xB = xB, xA
        for i in range(xA, xB+1):
            spaces.append([i, yA])
    else:
        if yA > yB:
            yA, yB = yB, yA
        for i in range (yA, yB+1):
            spaces.append([xA, i])
    placement_valid = check_collision(spaces, player_occupied_spaces)
    if placement_valid:
        for coordinate in spaces:
            occupied_spaces.append(coordinate)
    else:
        occupied_spaces = []
        slow_print("Ships can not hit each other! Please, try again placing them somewhere else. It's ok if your ships touch.")
        player_ship_placement()                  
 
def check_collision(spaces, occupied_spaces):
    for coordinate in spaces:
        if coordinate in occupied_spaces:
            return False
    return True
 
def update_grid(next_grid, occupied_spaces, sunken_spaces, shots_fired):
    next_grid = []
    for y in range(GRID_LENGTH): #  ???
        column = []
        for x in range(GRID_HEIGHT): # Why does it work with flipped x y?
            if [x, y] in sunken_spaces:
                column.append("!")
            elif [x, y] in occupied_spaces:
                column.append("V")
            elif [x, y] in shots_fired:
                column.append("X")
            else:
                column.append("o")
        next_grid.append(column)
    grid_printer(next_grid)
 
def grid_printer(grid):
    counter = 0
    print("    ", end="")
    for coord in range(GRID_LENGTH):
        print(X_COORDINATES[counter], end=" ")
        counter += 1
    print("\n")
    counter = 0
    for row in grid:
        print(Y_COORDINATES[counter], end="   ")
        counter += 1
        for column in row:
            print(column, end=" ")
        print()
 
def computer_ship_distribution(occupied_spaces):
    for ship in opponent_ships:
        while True:
            spaces = []
            xA = random.randint(0, len(X_COORDINATES)-1)
            yA = random.randint(0, len(Y_COORDINATES)-1)
 
            if random.randint(0,1):
                is_horizontal = True
            else:
                is_horizontal = False
            if is_horizontal:
                if xA + ship.size < len(X_COORDINATES):
                    xB = xA + ship.size
                else:
                    xB = xA - ship.size
                yB = yA
            else:
                xB = xA
                if yA + ship.size < len(Y_COORDINATES):
                   yB = yA + ship.size
                else:
                    yB = yA - ship.size
            if is_horizontal:
                if xA > xB:
                    xA, xB = xB, xA
                for i in range(xA, xB):
                    spaces.append([i, yA])
            else:
                if yA > yB:
                    yA, yB = yB, yA
                for i in range (yA, yB):
                    spaces.append([xA, i])
            placement_valid = check_collision(spaces, opponent_occupied_spaces)
            if placement_valid:
                for coordinate in spaces:
                    occupied_spaces.append(coordinate)
                break
            else:
                continue

def player_move():
    while True:
        xS, yS = square_validator()
        if [xS, yS] in player_shots_fired:
            slow_print("You have already shot here. Try somewhere else.")
            continue
        else:
            break

    slow_print("You shot on field {}.".format(X_COORDINATES[xS]+str(yS)))
    if [xS, yS] in opponent_occupied_spaces:
        slow_print("It's a hit!")
        opponent_sunken_spaces.append([xS, yS])
        player_shots_fired.append([xS, yS])
    else:
        slow_print("It's a miss!")
        player_shots_fired.append([xS, yS])
        
def check_if_game_over():
    if opponent_occupied_spaces in player_shots_fired or player_occupied_spaces in opponent_shots_fired:
        return True
    else:
        return False
 
def select_mode():
    slow_print("""This battleship game contains four modes:
 
Easy
Medium
Hard
Cheat (used to pwn other players)
 
Please select mode by typing one of the above.""")
    while True:
        mode = input()
        match mode.lower():
            case "easy":
                return "easy"
            case "medium":
                return "medium"
            case "hard":
                return "hard"
            case "god":
                return "god"
            case "cheat":
                return "cheat"
            case _:
                slow_print("You did something wrong. Please select mode by typing one of the above.")
 
def get_mode(mode):
    match mode.lower():
        case "easy":
            xS, yS = computer_easy()
        case "medium":
            xS, yS = computer_medium()
        case "hard":
            xS, yS = computer_hard()
    
    return xS, yS

def computer_easy():
    while True:
        xS, yS = random.randint(0, len(X_COORDINATES)-1), random.randint(0, len(Y_COORDINATES)-1)
        if [xS, yS] in opponent_shots_fired:
            continue
        opponent_shots_fired.append([xS, yS])
        return xS, yS
    
def computer_medium():
    pass

def computer_hard():
    pass

def computer_move(x, y):
    slow_print("Computer shot on field {}.".format(X_COORDINATES[x]+str(y)))
    if [x, y] in player_occupied_spaces:
        slow_print("It's a hit!")
        player_sunken_spaces.append([x, y])
        opponent_shots_fired.append([x, y])
    else:
        slow_print("It's a miss!")
        opponent_shots_fired.append([x, y])

def game_round():
    global game_over
    player_move()
    xS, yS = get_mode(mode)
    computer_move(xS, yS)
    game_over = check_if_game_over()
    update_grid(player_next_grid, player_occupied_spaces, player_sunken_spaces, player_shots_fired)
    print()
    update_grid(opponent_next_grid, opponent_occupied_spaces, opponent_sunken_spaces, opponent_shots_fired)

for x in range(GRID_LENGTH):
    column = []
    for y in range(GRID_HEIGHT):
        column.append("o")        
    player_next_grid.append(column)
    opponent_next_grid.append(column)
 
computer_ship_distribution(opponent_occupied_spaces)
player_ship_placement(player_ships)

while game_over is False:
    game_round()
 