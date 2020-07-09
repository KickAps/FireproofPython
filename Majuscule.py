import sys

# Get the phrase from argument
phrase = str(sys.argv[1])
final_phrase = ""

# Loop on the letter index of the phrase
for x in range(0, len(phrase)):
    if x % 2 == 0:
        # Add the letter in lowercase
        final_phrase += phrase[x].lower()
    else:
        # Add the letter in uppercase
        final_phrase += phrase[x].upper()

# Print final phrase
print(final_phrase)
