from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (books) and domain (positions 1 to 5, where 1 is leftmost)
books = ["blue", "purple", "yellow", "red", "gray"]
positions = range(1, 6)
problem.addVariables(books, positions)

# Add constraints based on the problem description
# 1. All books must be in different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The yellow book is to the right of the gray book" → yellow > gray
problem.addConstraint(lambda yellow, gray: yellow > gray, ("yellow", "gray"))

# 3. "The purple book is to the left of the gray book" → purple < gray
problem.addConstraint(lambda purple, gray: purple < gray, ("purple", "gray"))

# 4. "The red book is to the right of the blue book" → red > blue
problem.addConstraint(lambda red, blue: red > blue, ("red", "blue"))

# 5. "The purple book is the third from the left" → purple == 3
problem.addConstraint(lambda purple: purple == 3, ("purple",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to book names for the question about who is second from left (position 2)
choices = {
    "A": "blue",
    "B": "purple",
    "C": "yellow",
    "D": "red",
    "E": "gray"
}

# Find which book is at position 2 and print the corresponding choice letter
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 2:
            print(letter)