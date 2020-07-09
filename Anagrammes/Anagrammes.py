import sys


def word_to_dict(word_to_convert):
    """
    Convert a word in a dict of letters

    Parameters
    ----------
    word_to_convert The word to convert

    Returns
    -------
    The dict of letters

    """

    final_dict = {}
    for letter in word_to_convert:
        if letter in final_dict:
            final_dict[letter] += 1
        else:
            final_dict[letter] = 1

    return final_dict


def check_anagrams(word1, word2):
    """
    Check if the two words given are anagrams
    Print the words if they are

    Parameters
    ----------
    word1 The first word
    word2 The second word

    """
    anagram = False
    # Check the words size
    if len(word1) != len(word2):
        return

    dict1 = word_to_dict(word1)
    dict2 = word_to_dict(word2)

    for key in dict1:
        if key in dict2 and dict2[key] == dict1[key]:
            anagram = True
        else:
            anagram = False
            break

    if anagram:
        print(word1 + " : " + word2)


# Get arguments
if len(sys.argv) != 3:
    print("Two arguments needed : word file")
    exit()

word = sys.argv[1]
filename = sys.argv[2]

# Open the file
file = open(filename, 'r', encoding='utf-8')

for line in file.readlines():
    file_word = line.replace('\n', '')
    check_anagrams(word, file_word)

# Close the file
file.close()
