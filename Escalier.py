import sys

stepsNumber = 0

try:
    # Get the steps number from argument
    stepsNumber = int(sys.argv[1])
except ValueError:
    # If the argument is not an integer
    print("Wrong argument...")

# Loop from 1 to steps number
for i in range(1, stepsNumber + 1):
    print(" " * (stepsNumber - i) + "#" * i)
