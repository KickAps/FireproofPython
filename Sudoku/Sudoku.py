import sys
import copy
import os
from xlwt import Workbook


def file_to_array(file_to_convert):
    """
    Convert the sudoku from file to array

    Parameters
    ----------
    file_to_convert The file to convert

    Returns
    -------
    The sudoku in array format

    """

    final_array = []
    invalid_chars = ['|', '+', '-', '\n']

    for file_line in file_to_convert.readlines():
        tmp = []
        for number in file_line:
            if number not in invalid_chars:
                tmp.append(number)
        if len(tmp):
            final_array.append(tmp)

    return final_array


def get_square_pos(p_x, p_y):
    """
    Give all the numbers coordinates of the square containing the position given

    Parameters
    ----------
    p_x The x position
    p_y The y position

    Returns
    -------
    The list of the positions

    """

    tmp = []
    square_pos = [[p_x, p_y]]

    if p_x % 3 == 0:
        # 0 3 6 : x+1 x+2
        square_pos.extend([[p_x + 1, p_y], [p_x + 2, p_y]])
    elif p_x % 3 == 1:
        # 1 4 7 : x-1 x+1
        square_pos.extend([[p_x - 1, p_y], [p_x + 1, p_y]])
    elif p_x % 3 == 2:
        # 2 5 8 : x-2 x-1
        square_pos.extend([[p_x - 2, p_y], [p_x - 1, p_y]])

    if p_y % 3 == 0:
        for pos in square_pos:
            tmp.extend([[pos[0], pos[1] + 1], [pos[0], pos[1] + 2]])
    elif p_y % 3 == 1:
        for pos in square_pos:
            tmp.extend([[pos[0], pos[1] - 1], [pos[0], pos[1] + 1]])
    elif p_y % 3 == 2:
        for pos in square_pos:
            tmp.extend([[pos[0], pos[1] - 2], [pos[0], pos[1] - 1]])

    square_pos.extend(tmp)

    return square_pos


def get_possibilities(p_sudoku, p_x, p_y):
    """
    Get all possibilities for a given position in the sudoku

    Parameters
    ----------
    p_sudoku    The sudoku
    p_x         The x position
    p_y         The y position

    Returns
    -------
    The list of the available numbers for a position in the sudoku

    """

    available_numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

    # Line check
    for number in p_sudoku[p_y]:
        if number != '_' and number in available_numbers:
            available_numbers.remove(number)

    # Column check
    for line in p_sudoku:
        number = line[p_x]
        if number != '_' and number in available_numbers:
            available_numbers.remove(number)

    # Square check
    square_pos = get_square_pos(p_x, p_y)
    for pos in square_pos:
        number = p_sudoku[pos[1]][pos[0]]
        if number != '_' and number in available_numbers:
            available_numbers.remove(number)

    return available_numbers


def get_resolution_order(p_sudoku, pos_list):
    """
    Get the resolution order of the sudoku

    Parameters
    ----------
    p_sudoku The sudoku
    pos_list The list of positions of missing numbers

    Returns
    -------
    The possibilities sorted

    """

    pos_list_tmp = copy.deepcopy(pos_list)
    pos_list.clear()
    possibilities = {}
    for pos in pos_list_tmp:
        possibilities[(pos[0], pos[1])] = get_possibilities(p_sudoku, pos[0], pos[1])

    # Sort the positions of missing numbers by the number of possibilities
    for i in range(1, 10):
        for pos in pos_list_tmp:
            possibility = possibilities[(pos[0], pos[1])]
            if len(possibility) == i:
                pos_list.append(pos)

    return possibilities


def check_number(p_sudoku, p_x, p_y):
    """
    Check if the number is correct in the sudoku

    Parameters
    ----------
    p_sudoku    The sudoku
    p_x         The x position
    p_y         The y position

    Returns
    -------
    True if number is correct
    False if not

    """

    current_number = p_sudoku[p_y][p_x]

    # Line check
    for x, number in enumerate(p_sudoku[p_y]):
        if x == p_x:
            continue
        if number != '_' and number == current_number:
            return False

    # Column check
    for y, line in enumerate(p_sudoku):
        if y == p_y:
            continue
        number = line[p_x]
        if number != '_' and number == current_number:
            return False

    # Square check
    square_pos = get_square_pos(p_x, p_y)
    for pos in square_pos:
        if pos[0] == p_x and pos[1] == p_y:
            continue
        number = p_sudoku[pos[1]][pos[0]]
        if number != '_' and number == current_number:
            return False

    return True


def try_possibilities(p_sudoku, pos_list, possibilities, possibilities_backup, index, recursive_calls):
    """

    Try the possibilities given

    Parameters
    ----------
    p_sudoku                The sudoku to solve
    pos_list                The list of the missing numbers positions
    possibilities           The possibilities dictionary for each position (mission numbers)
    possibilities_backup    Backup of the possibilities dictionary
    index                   The index of the current position
    recursive_calls         The number of recursive calls (stats)

    """

    recursive_calls.append(index)
    x, y = pos_list[index]
    possibility = possibilities[(x, y)]
    possibility_copy = copy.deepcopy(possibility)

    # Loop on the possibilities
    for number in possibility_copy:
        p_sudoku[y][x] = number
        possibility.remove(number)

        if check_number(p_sudoku, x, y):
            if index < len(pos_list) - 1:
                # Recursive call to the next number
                try_possibilities(p_sudoku, pos_list, possibilities, possibilities_backup, index + 1, recursive_calls)
            return

    # Case of backtracking and all the previous numbers have already been checked
    if index > 0:
        # Backup the possibilities
        possibilities[(x, y)] = copy.deepcopy(possibilities_backup[(x, y)])
        # Reset the number in the sudoku
        p_sudoku[y][x] = '_'
        # Recursive call to the previous number
        try_possibilities(p_sudoku, pos_list, possibilities, possibilities_backup, index - 1, recursive_calls)
    else:
        # The sudoku can't be solved
        print("Resolution failed...")
    return


def solve_sudoku(p_sudoku):
    """
    Solve the sudoku given

    Parameters
    ----------
    p_sudoku The sudoku to solve

    """

    pos_list = []

    # Find the position of missing numbers
    for y, line in enumerate(p_sudoku):
        for x, number in enumerate(line):
            if number == '_':
                pos_list.append([x, y])

    # Get the resolution order of the missing numbers
    possibilities = get_resolution_order(p_sudoku, pos_list)
    possibilities_backup = copy.deepcopy(possibilities)

    recursive_calls = []
    try_possibilities(p_sudoku, pos_list, possibilities, possibilities_backup, 0, recursive_calls)

    print("Missing numbers : " + str(len(pos_list)) + "/81")
    print("Recursive calls : " + str(len(recursive_calls)))

    # Save the stats in excel
    excel = Workbook()
    sheet = excel.add_sheet("stats")

    for index, number in enumerate(recursive_calls):
        sheet.write(index, 0, index)
        sheet.write(index, 1, number)

    excel_path = os.path.dirname(os.path.abspath(__file__)) + "/stats.xls"

    if os.path.isfile(excel_path):
        os.remove(excel_path)
    excel.save(excel_path)


def print_sudoku(p_sudoku):
    """
    Print the sudoku given

    Parameters
    ----------
    p_sudoku The sudoku to print

    """

    sudoku_string = ""
    print(" ")
    for y, column in enumerate(p_sudoku):
        if y != 0 and y % 3 == 0:
            sudoku_string += "---+---+---\n"

        for x, number in enumerate(p_sudoku[y]):
            if x != 0 and x % 3 == 0:
                sudoku_string += '|'
            sudoku_string += number

        sudoku_string += '\n'
    print(sudoku_string)


# Get arguments
if len(sys.argv) != 2:
    print("One argument needed : file")
    exit()

filename = sys.argv[1]
file = object

try:
    file = open(filename, 'r', encoding='utf-8')
except IOError:
    print("Wrong argument...")
    exit()

sudoku = file_to_array(file)

# Print the sudoku before resolution
print_sudoku(sudoku)

# If the solutions sorting part is not done, the recursion limit must be increase (just a test)
# sys.setrecursionlimit(3000)

solve_sudoku(sudoku)

# Print the sudoku after resolution
print_sudoku(sudoku)
