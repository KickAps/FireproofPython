import sys
import os


def file_to_array(file):
    """
    Convert a file in list of lines

    Parameters
    ----------
    file The file to convert

    Returns
    -------
    The array of lines

    """

    array = []
    # Reset the file cursor
    file.seek(0)
    for line in file.readlines():
        array.append(line.replace('\n', ''))

    return array


# Get arguments
file_name1 = sys.argv[1]
file_name2 = sys.argv[2]

# Test if the files exist
if not os.path.isfile(file_name1) or not os.path.isfile(file_name2):
    print("Wrong argument...")
    exit()

# Open the files
file1 = open(file_name1, 'r', encoding='utf-8')
file2 = open(file_name2, 'r', encoding='utf-8')

# Read the files
print(file1.read()+'\n')
print(file2.read()+'\n')

# Convert the files
array_file1 = file_to_array(file1)
array_file2 = file_to_array(file2)

match = False
# Loop on lines of file 2
for i, string2 in enumerate(array_file2):
    pos_x = string2.find(array_file1[0])
    if pos_x != -1:
        pos_y = i
        # Loop on lines of file 1
        for j, string1 in enumerate(array_file1):
            if array_file2[i+j].find(string1) == pos_x:
                match = True
                continue
            else:
                match = False
                break

        # The file 2 contains fully the file 1
        if match:
            break

if match:
    print("Position: " + str(pos_x) + "," + str(pos_y))
else:
    print("No match...")

# Close the files
file1.close()
file2.close()
