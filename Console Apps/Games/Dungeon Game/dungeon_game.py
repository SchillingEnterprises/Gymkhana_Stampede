import logging
import os
import random


logging.basicConfig(filename='game.log', level=logging.DEBUG)

player = {'location': None, 'path': []}
CELLS = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0),
         (0, 1), (1, 1), (2, 1), (3, 1), (4, 1),
         (0, 2), (1, 2), (2, 2), (3, 2), (4, 2),
         (0, 3), (1, 3), (2, 3), (3, 3), (4, 3),
         (0, 4), (1, 4), (2, 4), (3, 4), (4, 4)]


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


# pick random location for player
# pick random location for exit door
# pick random location for the monster
def get_locations():
    monster = random.choice(CELLS)
    door = random.choice(CELLS)
    start = random.choice(CELLS)

    if monster == door or monster == start or door == start:
        monster, door, start = get_locations()

    return monster, door, start


# move player, unless invalid move (past edges of grid)
def move_player(player, move):
    x, y = player['location']
    player['path'].append((x, y))

    if move == 'LEFT':
        player['location'] = x, y - 1
    elif move == 'UP':
        player['location'] = x - 1, y
    elif move == 'RIGHT':
        player['location'] = x, y + 1
    elif move == 'DOWN':
        player['location'] = x + 1, y

    return player


def get_moves(player):
    moves = ["LEFT", "RIGHT", "UP", "DOWN"]
    x, y = player

    # if player's x = 0, they can't move left
    if x == 0:
        moves.remove("LEFT")

    # if player's x = 4, they can't move right
    if x == 4:
        moves.remove("RIGHT")

    # if player's y = 0, they can't move up
    if y == 0:
        moves.remove("UP")

    # if player's y = 4, they can't move down
    if y == 4:
        moves.remove("DOWN")

    return moves


# draw grid
def draw_map(player):
    print(" _" * 5)
    tile = "|{}"

    for cell in CELLS:
        x, y = cell
        if x < 4:
            line_end = ""
            if cell == player:
                # draw player in the grid
                output = tile.format("X")
            else:
                output = tile.format("_")
        else:
            line_end = "\n"
            if cell == player:
                # draw player in the grid
                output = tile.format("X|")
            else:
                output = tile.format("_|")
        print(output, end=line_end)


monster, door, player['location'] = get_locations()
logging.info('monster: {}; door: {}; player: {}'
             .format(monster, door, player['location']))


print("Welcome to the dungeon!")
input("Press return to start!")
clear_screen()


while True:
    moves = get_moves(player['location'])
    clear_screen()
    print("You're currently in room {}".format(player['location']))

    draw_map(player)

    print("\nYou can move {}".format(', '.join(moves)))
    print("Enter QUIT to quit")

    move = input("> ")
    move = move.upper()

    if move == 'QUIT':
        break

    if move not in moves:
        print("\n** Walls are hard! Stop running into them! **\n")
        continue

    player = move_player(player, move)
    if player['location'] == door:
        print("\n** You escaped! **\n")
        break
    elif player['location'] == monster:
        print("\n** You got eaten! **\n")
        break
    else:
        continue
