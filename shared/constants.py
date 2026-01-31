# constants.py

# chunk size important
CHUNK_SIZE = 16

WALKABLE = {"minecraft:air", "minecraft:grass", "minecraft:dirt", }

# movement_costs.py
MOVEMENT_COST = {
    "minecraft:air": 1,
    "minecraft:grass": 1,
    "minecraft:dirt": 2,
    "minecraft:sand": 3,
    "minecraft:gravel": 4,
    "minecraft:stone": None,  # None = blocked
}

NEIGHBORS = [
    (1, 0, 0), (-1, 0, 0),
    (0, 0, 1), (0, 0, -1),

    # diagonals
    (1, 0, 1), (1, 0, -1),
    (-1, 0, 1), (-1, 0, -1),

    # vertical
    (0, 1, 0),  # up
    (0, -1, 0),  # down
]
