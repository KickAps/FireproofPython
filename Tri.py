# TEST : python Tri.py 10 9 8 7 6 5 4 3 2 1 100 11 20 -4 1000 156 132 148
import sys


def partition(list_to_sort, start, end):
    """
    Sort the given list of numbers between 'start' and 'end'

    Parameters
    ----------
    list_to_sort The list of numbers to sort
    start The start cursor
    end The end cursor

    Returns
    -------
    The pivot cursor

    """
    pivot_index = end
    cursor = start

    # print("(" + str(start) + "," + str(end) + ")") # DEBUG
    # print("PIVOT= "+str(list_to_sort[pivot_index])) # DEBUG
    # print("1: "+str(list_to_sort)) # DEBUG

    # Loop from start to end cursor
    for i in range(start, end + 1):
        if list_to_sort[i] < list_to_sort[pivot_index]:
            if list_to_sort[i] < list_to_sort[cursor]:
                tmp = list_to_sort[i]
                list_to_sort[i] = list_to_sort[cursor]
                list_to_sort[cursor] = tmp
                # print("2: "+str(list_to_sort)) # DEBUG
            cursor += 1

    tmp = list_to_sort[cursor]
    list_to_sort[cursor] = list_to_sort[pivot_index]
    list_to_sort[pivot_index] = tmp
    # print("3: "+str(list_to_sort)) # DEBUG
    return cursor


def quick_sort(list_to_sort, start, end):
    """
    Recursive quick sort

    Parameters
    ----------
    list_to_sort The list of numbers to sort
    start The start cursor
    end The end cursor

    """
    if end >= start:
        pivot_index = partition(list_to_sort, start, end)
        # Recursive calls
        quick_sort(list_to_sort, start, pivot_index - 1)
        quick_sort(list_to_sort, pivot_index + 1, end)


numbersList = []
correct = True

for x in range(1, len(sys.argv)):
    try:
        numbersList.append(int(sys.argv[x]))
    except ValueError:
        print(sys.argv[x] + " : wrong argument...")
        correct = False

if not correct:
    sys.exit()

quick_sort(numbersList, 0, len(numbersList) - 1)
print(numbersList)
