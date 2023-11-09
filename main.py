"""BATTLESHIPS"""
 
from print_enchancer import *
from ships import Ship
import random
import sys
import copy
 
GRID_LENGTH = 10
GRID_HEIGHT = 10
X_COORDINATES = "ABCDEFGHIJ"
Y_COORDINATES = "0123456789"
 
game_mode = ""
game_over = False
winner = ""
did_opponent_hit = False
 
player_next_grid = []
player_occupied_spaces = []
player_sunken_spaces = []
player_shots_fired = []
opponent_next_grid = []
opponent_occupied_spaces = []
opponent_sunken_spaces = []
opponent_shots_fired = []
opponent_known_ships = []
 
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
 
starting_message = ("""Welcome to Battleships!
 
Rules are simple:
Both you and your opponent have a 10x10 squares grid, on which you place your ships:
2 spaces big Destroyer,
3 spaces big Cruiser,
3 spaces big Submarine,
4 spaces big Battleship,
and 5 spaces big Aircraft Career.
 
You start by positioning your ships on your board. Ships can touch, but cannot overlap.
After that, you are presented two boards: one yours, with ships shown to you (ships are represented by "V" on the board),
And second - opponents' - who's ships are hidden.
You both take turns on shooting one square. 
After shooting, you get the info whether your shot hit(represented by "!"), or missed(represented by "X").
After taking down a ship, you get the info that the ship has sunk.
 
Your goal is to take down all opponents' ships before they take down all yours!
You can play against a computer, or access a mode where the computer will help you out on winning against others,
Using the most efficient ways!
""")
 
def square_validator(move):
    while True:
        if len(move) != 2:
            slow_print("This is not a valid square. Try again.")
            move = input()
        if move.upper()[0] in X_COORDINATES and move[1] in Y_COORDINATES:
            x, y = X_COORDINATES.find(move[0].upper()), int(move[1])
            square_valid = True
            return x, y, square_valid
        else:
            square_valid = False
            return 0, 0, square_valid
 
def check_coordinates():
    move = ""
    move = input()
    if len(move) == 2:
        xA, yA, validA = square_validator(move)
        slow_print("Where do you want it to end?")
        move = input()
        xB, yB, validB = square_validator(move)
        return xA, yA, xB, yB
    elif len(move) == 4:
        A, B = move[0:2], move[2:4]
        xA, yA, validA = square_validator(A)
        xB, yB, validB = square_validator(B)
        if validA and validB:      
            return xA, yA, xB, yB
        else:
            slow_print("This is not a valid square. Try again.")
            check_coordinates()
    else:
        slow_print("This is not a valid square. Try again.")
        check_coordinates()
 
def player_ship_placement(ship_list):
    for ship in ship_list:
        xA, yA, xB, yB, is_horizontal = ship_placement_validator(ship)
        ship.pointA = [xA, yA]
        ship.pointB = [xB, yB]
        ship.is_horizontal = is_horizontal
        update_grid(player_next_grid, player_occupied_spaces, player_sunken_spaces, player_shots_fired, "player")
 
def ship_placement_validator(ship):    
    slow_print("\n{} is {} spaces big.".format(ship.name, ship.size))
    while True:
        slow_print("\nWhere do you want it to start?")
        xA, yA, xB, yB = check_coordinates()
        if xA == xB and yA != yB:
            if abs(yA - yB) == ship.size - 1:
                is_horizontal = False
                add_ship_coordinates(xA, yA, xB, yB, is_horizontal, player_occupied_spaces, ship)
                slow_print(f"{ship.name}'s coordinates are [{X_COORDINATES[xA]+str(yA)}, {X_COORDINATES[xB]+str(yB)}]")
                return xA, yA, xB, yB, is_horizontal
            else:
                slow_print("{} can't be placed that way. Remember, it is {} spaces big.".format(ship.name, ship.size))               
        elif yA == yB and xA != xB:
            if abs(xA - xB) == ship.size - 1:
                is_horizontal = True
                add_ship_coordinates(xA, yA, xB, yB, is_horizontal, player_occupied_spaces, ship)
                slow_print(f"{ship.name}'s coordinates are [{X_COORDINATES[xA]+str(yA)}, {X_COORDINATES[xB]+str(yB)}]")
                return xA, yA, xB, yB, is_horizontal              
            else:
                slow_print("{} can't be placed that way. Remember, it is {} spaces big.".format(ship.name, ship.size))          
        else:
            fast_print("""This is not a valid position for a ship.
Remember that the ships can only be placed vertically or horizontally (not diagonally).
Please enter valid ship positioning.""")
 
def add_ship_coordinates(xA, yA, xB, yB, is_horizontal, occupied_spaces, ship):
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
            ship.initial_coordinates.append(coordinate)
            ship.afloat_coordinates.append(coordinate)
    else:
        occupied_spaces = []
        slow_print("Ships can not hit each other! Please, try again placing them somewhere else. It's ok if your ships touch.")
        player_ship_placement(player_ships)                  
 
def check_collision(spaces, occupied_spaces):
    for coordinate in spaces:
        if coordinate in occupied_spaces:
            return False
    return True
 
def update_grid(next_grid, occupied_spaces, sunken_spaces, shots_fired, grid_owner):
    next_grid = []
    for y in range(GRID_LENGTH): #  ???
        column = []
        for x in range(GRID_HEIGHT): # Why does it work with flipped x y?
            if [x, y] in sunken_spaces:
                column.append("!")
            elif [x, y] in occupied_spaces and grid_owner == "player":
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
                if xA > xB:
                    xA, xB = xB, xA
                for i in range(xA, xB):
                    spaces.append([i, yA])
            else:
                xB = xA
                if yA + ship.size < len(Y_COORDINATES):
                   yB = yA + ship.size
                else:
                    yB = yA - ship.size
                if yA > yB:
                    yA, yB = yB, yA
                for i in range (yA, yB):
                    spaces.append([xA, i])
            placement_valid = check_collision(spaces, opponent_occupied_spaces)
            if placement_valid:
                for coordinate in spaces:
                    occupied_spaces.append(coordinate)
                    ship.initial_coordinates.append(coordinate)
                    ship.afloat_coordinates.append(coordinate)
                break
            else:
                continue
 
def player_move():
    while True:
        slow_print("Where do you want to shoot?")
        move = input()
        xS, yS, validS = square_validator(move)
        if not validS:
            continue
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
    global winner
    sunk_ships = 0
    for ship in opponent_ships:
        if ship.afloat_coordinates == []:
            sunk_ships += 1
        if sunk_ships == 5:
            winner = "player"
            return True
    sunk_ships = 0
    for ship in player_ships:
        if ship.afloat_coordinates == []:
            sunk_ships += 1
        if sunk_ships == 5:
            winner = "opponent"
            return True
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
 
def get_mode(game_mode):
    match game_mode.lower():
        case "easy":
            xS, yS = computer_easy()
        case "medium":
            xS, yS = computer_medium()
        case "hard":
            xS, yS = computer_hard()
        case "god":
            xS, yS = computer_god()
    return xS, yS
 
def computer_easy():
    """This is just dumb random shooting computer"""
 
    while True:
        xS, yS = random.randint(0, len(X_COORDINATES)-1), random.randint(0, len(Y_COORDINATES)-1)
        if [xS, yS] in opponent_shots_fired:
            continue
        return xS, yS
 
def computer_medium():
    """This uses a hunt and target algorithm."""
    global opponent_known_ships
 
    opponent_unknown_ships = copy.deepcopy(player_sunken_spaces) #  This single line was the hardest part in the whole project.

    vectors = ["up", "down", "left", "right"]
 
    for coordinate in opponent_unknown_ships:
        if coordinate in opponent_known_ships:
            opponent_unknown_ships.remove(coordinate)
 
    for ship in player_ships:
        if not ship.afloat:
            for coordinate in ship.initial_coordinates:
                if coordinate not in opponent_known_ships:
                    opponent_known_ships.append(coordinate)
                if coordinate in opponent_unknown_ships:
                    opponent_unknown_ships.remove(coordinate)
 
    while not opponent_unknown_ships:
        xS, yS = random.randint(0, len(X_COORDINATES)-1), random.randint(0, len(Y_COORDINATES)-1)
        if [xS, yS] in opponent_shots_fired:
            continue
        return xS, yS
 
    target_square = -1
    did_deduce = False

    while opponent_unknown_ships:
        current_target = copy.copy(opponent_unknown_ships[target_square])
        if len(opponent_unknown_ships) >= 2:
            if abs(current_target[0] - opponent_unknown_ships[target_square-1][0]) >= 1 and not did_deduce:
                vectors = ["left", "right"]
                did_deduce = True
            elif abs(current_target[1] - opponent_unknown_ships[target_square-1][1]) >= 1 and not did_deduce:
                vectors = ["up", "down"]
                did_deduce = True
 
        if not vectors:
            vectors = ["up", "down", "left", "right"]
            target_square += 1
            did_deduce = False
            continue
 
        vector = random.choice(vectors)
        match vector:      
            case "up":
                current_target[1] = current_target[1] - 1
                if current_target[1] < 0:
                    vectors.remove(vector)
                    continue
                if [current_target[0], current_target[1]] in opponent_shots_fired:
                    vectors.remove(vector)
                    continue
                return current_target[0], current_target[1] 
            case "down":
                current_target[1] = current_target[1] + 1
                if current_target[1] > 9:
                    vectors.remove(vector)
                    continue
                if [current_target[0], current_target[1]] in opponent_shots_fired:
                    vectors.remove(vector)
                    continue
                return current_target[0], current_target[1]   
            case "left":
                current_target[0] = current_target[0] - 1
                if current_target[0] < 0:
                    vectors.remove(vector)
                    continue  
                if [current_target[0], current_target[1]] in opponent_shots_fired:
                    vectors.remove(vector)
                    continue
                return current_target[0], current_target[1] 
            case "right":
                current_target[0] = current_target[0] + 1
                if current_target[0] > 9:
                    vectors.remove(vector)
                    continue
                if [current_target[0], current_target[1]] in opponent_shots_fired:
                    vectors.remove(vector)
                    continue
                return current_target[0], current_target[1] 
 
def computer_hard():
    """This uses hunt and target algorithm combined with probability heatmap."""
    
    opponent_unknown_ships = copy.deepcopy(player_sunken_spaces)

    for coordinate in opponent_unknown_ships:
        if coordinate in opponent_known_ships:
            opponent_unknown_ships.remove(coordinate)
 
    for ship in player_ships:
        if not ship.afloat:
            for coordinate in ship.initial_coordinates:
                if coordinate not in opponent_known_ships:
                    opponent_known_ships.append(coordinate)
                if coordinate in opponent_unknown_ships:
                    opponent_unknown_ships.remove(coordinate)

    if opponent_unknown_ships:
        computer_medium()
    else:
        heatmap = {}
        for x in range(GRID_LENGTH):
            for y in range(GRID_HEIGHT):
                map.update({(x, y): 0})

 
def computer_god():
    """This just shoots your ships down one by one. Why would anyone play that?"""
 
    while True:
        attack = random.randint(0,len(player_occupied_spaces)-1)
        if player_occupied_spaces[attack] not in player_sunken_spaces:
            xS, yS = player_occupied_spaces[attack]
            return xS, yS
 
def computer_move(x, y):
    global did_opponent_hit, player_sunken_spaces 
    slow_print("Computer shot on field {}.".format(X_COORDINATES[x]+str(y)))
    if [x, y] in player_occupied_spaces:
        slow_print("It's a hit!")
        player_sunken_spaces.append([x, y])
        opponent_shots_fired.append([x, y])
        did_opponent_hit = True
    else:
        slow_print("It's a miss!")
        opponent_shots_fired.append([x, y])
        did_opponent_hit = False
 
def previously_hit(target):
    return True if target in opponent_shots_fired else False
 
def check_if_ship_sunk(ship_list, shots_fired):
    for ship in ship_list:
        for coordinate in ship.afloat_coordinates:
            if coordinate in shots_fired:
                ship.afloat_coordinates.remove(coordinate)
        if ship.afloat_coordinates == [] and ship.afloat:
            ship.afloat = False
            slow_print("{}'s {} has sunk!".format(ship.owner.capitalize(), ship.name))
 
def game_round():
    global game_over
    player_move()
    check_if_ship_sunk(opponent_ships, player_shots_fired)
    xS, yS = get_mode(game_mode)
    computer_move(xS, yS)
    check_if_ship_sunk(player_ships, opponent_shots_fired)
    game_over = check_if_game_over()
    update_grid(player_next_grid, player_occupied_spaces, player_sunken_spaces, opponent_shots_fired, "player")
    print()
    update_grid(opponent_next_grid, opponent_occupied_spaces, opponent_sunken_spaces, player_shots_fired, "opponent")
 
if __name__ == "__main__":
 
    for x in range(GRID_LENGTH):
        column = []
        for y in range(GRID_HEIGHT):
            column.append("o")        
        player_next_grid.append(column)
        opponent_next_grid.append(column)
 
 
    #slow_print(starting_message)
    #game_mode = select_mode()
    game_mode = "medium"
    computer_ship_distribution(opponent_occupied_spaces)
    update_grid(player_next_grid, player_occupied_spaces, player_sunken_spaces, player_shots_fired, "player")
    slow_print("\nYou can enter one or both coordinates (without spaces) of ship at a time.")
    player_ship_placement(player_ships)
 
    while not game_over:
        game_round()
    print("GOWNO KUWA")
    sys.exit()
 