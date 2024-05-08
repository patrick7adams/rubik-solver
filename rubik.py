from enum import Enum
import random

board_dict = {
    1: "\033[0;31m",
    2: "\033[0;32m",
    3: "\033[0;34m",
    4: "\033[1;33m",
    5: "\033[1;37m",
    6: "\033[1;31m",
}

possible_moves = ["U", "U'", "D", "D'", "L", "L'", "R", "R'", "F", "F'", "B", "B'"]
completed_moves = []

board = [[i for k in range(9)] for i in range(1, 7)]


class BoardSides(Enum):
    U = 5
    L = 1
    F = 2
    R = 6
    B = 3
    D = 4
    WHITE = 5
    ORANGE = 1
    GREEN = 2
    RED = 6
    BLUE = 3
    YELLOW = 4


def print_board(board):
    side_print_dict = {
        (0, 1): BoardSides.U.value,
        (1, 0): BoardSides.L.value,
        (1, 1): BoardSides.F.value,
        (1, 2): BoardSides.R.value,
        (1, 3): BoardSides.B.value,
        (2, 1): BoardSides.D.value,
    }
    s = ""
    for row in range(3):
        for i in range(3):
            for col in range(4):
                for k in range(3):
                    side = side_print_dict.get((row, col))
                    if side:
                        s += board_dict[board[side - 1][convert((i, k))]] + "[]"
                    else:
                        s += "  "
            s += "\n"
    print(s)

def copy(board):
    return [[board[i][k] for k in range(9)] for i in range(6)]

def convert(coords):
    return coords[0] * 3 + coords[1]


def get(board, side, coords):
    return board[side - 1][convert(coords)]


def get_multiple(board, side, coords):
    return [board[side - 1][convert(item)] for item in coords]


def is_equal(board, side, coords, color):
    return True if get(board, side, coords) == color else False


def all_is_equal(board, side, coords, color):
    return True if all(is_equal(board, side, item, color) for item in coords) else False


def set(board, side, coords, new_color):
    board[side - 1][convert(coords)] = new_color


def set_from_coords(board, side, coords, new_side, new_coords):
    board[side - 1][convert(coords)] = get(board, new_side, new_coords)


def rotate_side(board, side, inv=False):
    # CW: (0, 0) -> (2, 0) -> (2, 2) -> (0, 2)
    #     (1, 0) -> (2, 1) -> (1, 2) -> (0, 1)
    swap_order_edge = [(0, 0), (2, 0), (2, 2), (0, 2)]
    swap_order_corner = [(1, 0), (2, 1), (1, 2), (0, 1)]
    if inv:
        swap_order_edge.reverse()
        swap_order_corner.reverse()
    tmp_edge = get(board, side, swap_order_edge[0])
    tmp_corner = get(board, side, swap_order_corner[0])
    for i in range(len(swap_order_edge) - 1):
        # print(f"Swapping {swap_order_edge[i+1]} with {swap_order_edge[i]}")
        # print(f"Swapping {swap_order_corner[i+1]} with {swap_order_corner[i]}")
        set_from_coords(board, side, swap_order_edge[i], side, swap_order_edge[i + 1])
        set_from_coords(
            board, side, swap_order_corner[i], side, swap_order_corner[i + 1]
        )
        # print_board(board)
    set(board, side, swap_order_edge[-1], tmp_edge)
    set(board, side, swap_order_corner[-1], tmp_corner)


def rotate_edges(board, side, inv):
    def inc_config(coord, config, amt):
        match (config):
            case 1:
                return (coord[0] + amt, coord[1])
            case 2:
                return (coord[0], coord[1] + amt)
            case 3:
                return (coord[0] - amt, coord[1])
            case 4:
                return (coord[0], coord[1] - amt)

    rotations, configs, rot_configs = [], [], []
    if side == BoardSides.F.value or side == BoardSides.B.value:
        rotations = [
            BoardSides.U.value,
            BoardSides.R.value,
            BoardSides.D.value,
            BoardSides.L.value,
        ]
        configs = [(2, 0), (0, 0), (0, 2), (2, 2)]
        rot_configs = [2, 1, 4, 3]
        if side == BoardSides.B.value:
            configs = [(0, 0), (0, 2), (2, 2), (2, 0)]
        if side == BoardSides.F.value and not inv or side == BoardSides.B.value and inv:
            configs.reverse()
            rot_configs.reverse()
            rotations.reverse()
    if side == BoardSides.L.value or side == BoardSides.R.value:
        rotations = [
            BoardSides.F.value,
            BoardSides.U.value,
            BoardSides.B.value,
            BoardSides.D.value,
        ]
        configs = [(2, 2), (2, 2), (0, 0), (2, 2)]
        rot_configs = [3, 3, 1, 3]
        if side == BoardSides.L.value:
            configs = [(2, 0), (2, 0), (0, 2), (2, 0)]
        if side == BoardSides.L.value and inv or side == BoardSides.R.value and not inv:
            configs.reverse()
            rot_configs.reverse()
            rotations.reverse()
    if side == BoardSides.U.value or side == BoardSides.D.value:
        rotations = [
            BoardSides.F.value,
            BoardSides.R.value,
            BoardSides.B.value,
            BoardSides.L.value,
        ]
        configs = [(0, 0), (0, 0), (0, 0), (0, 0)]
        rot_configs = [2, 2, 2, 2]
        if side == BoardSides.D.value:
            configs = [(2, 0), (2, 0), (2, 0), (2, 0)]
        if side == BoardSides.D.value and not inv or side == BoardSides.U.value and inv:
            rotations.reverse()

    tmp_values = [
        get(board, rotations[0], inc_config(configs[0], rot_configs[0], i))
        for i in range(3)
    ]
    for i in range(3):
        for k in range(3):
            set_from_coords(
                board,
                rotations[i],
                inc_config(configs[i], rot_configs[i], k),
                rotations[i + 1],
                inc_config(configs[i + 1], rot_configs[i + 1], k),
            )
    for i in range(3):
        set(
            board,
            rotations[-1],
            inc_config(configs[-1], rot_configs[-1], i),
            tmp_values[i],
        )


def string_to_moves(board, str, record_moves=True):
    char_dict = {
        "U": (board, BoardSides.U.value, False),
        "U'": (board, BoardSides.U.value, True),
        "D": (board, BoardSides.D.value, False),
        "D'": (board, BoardSides.D.value, True),
        "L": (board, BoardSides.L.value, False),
        "L'": (board, BoardSides.L.value, True),
        "R": (board, BoardSides.R.value, False),
        "R'": (board, BoardSides.R.value, True),
        "F": (board, BoardSides.F.value, False),
        "F'": (board, BoardSides.F.value, True),
        "B": (board, BoardSides.B.value, False),
        "B'": (board, BoardSides.B.value, True),
    }
    for char in str.split():
        rotate_side(*char_dict[char])
        rotate_edges(*char_dict[char])


def randomize(board):
    num_randomizing_moves = 50
    str = " ".join(random.choice(possible_moves) for i in range(num_randomizing_moves))
    string_to_moves(board, str, record_moves=False)


def check_white_cross(board):
    if (
        all_is_equal(
            board,
            BoardSides.U.value,
            ((0, 1), (1, 0), (2, 1), (1, 2)),
            BoardSides.WHITE.value,
        )
        and is_equal(board, BoardSides.F.value, (0, 1), BoardSides.GREEN.value)
        and is_equal(board, BoardSides.R.value, (0, 1), BoardSides.RED.value)
        and is_equal(board, BoardSides.B.value, (0, 1), BoardSides.BLUE.value)
        and is_equal(board, BoardSides.L.value, (0, 1), BoardSides.ORANGE.value)
    ):
        return True
    return False


def find_white_cross(board, depth=0, depth_limit=6):
    # recursive search for the white cross
    if check_white_cross(board):
      return True
    elif depth == depth_limit:
      return False
          
    boards = []
    for move in possible_moves:
        new_board = copy(board)
        string_to_moves(new_board, move)
        boards.append(new_board)
        if find_white_cross(new_board, depth=depth+1, depth_limit=depth_limit):
            return new_board
        

# print(is_equal(board, BoardSides.U.value, (0, 1), BoardSides.WHITE.value))
randomize(board)
print_board(board)
print_board(find_white_cross(board))
