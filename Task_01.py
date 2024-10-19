def fibonacci_generator(n):
    fib_sequence = [0, 1]

    # Generate the sequence up to 'n' numbers
    for i in range(2, n):
        next_number = fib_sequence[i - 1] + fib_sequence[i - 2]
        fib_sequence.append(next_number)

    return fib_sequence


# Input: number of terms to generate
num_terms = int(input("Enter the number of terms in Fibonacci series: "))

# Generate and print Fibonacci sequence
if num_terms <= 0:
    print("Please enter a positive integer.")
elif num_terms == 1:
    print([0])
else:
    result = fibonacci_generator(num_terms)
    print(result)
