import sys

number = 0

try:
    number = int(sys.argv[1])

except ValueError:
    print("Wrong argument...")

# Raise an exception
assert(number >= 0), "The number must be positive..."


def recursive_factorial(p_number, p_result):
    if p_number == 0:
        string_result = ""
        for i, digit in enumerate(str(p_result)[::-1]):
            string_result += digit
            if (i + 1) % 3 == 0:
                string_result += ','

        print(string_result[::-1])

    else:
        # First call
        if p_result == 0:
            p_result = p_number
        # Then
        else:
            p_result *= p_number
            
        # Recursive call
        recursive_factorial(p_number-1, p_result)


recursive_factorial(number, 0)
