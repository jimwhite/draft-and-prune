from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
books = ["blue", "purple", "yellow", "red", "gray"]
positions = range(1, 6)
problem.addVariables(books, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The yellow book is to the right of the gray book"
problem.addConstraint(lambda yellow, gray: yellow > gray, ("yellow", "gray"))

# "The purple book is to the left of the gray book"
problem.addConstraint(lambda purple, gray: purple < gray, ("purple", "gray"))

# "The red book is to the right of the blue book"
problem.addConstraint(lambda red, blue: red > blue, ("red", "blue"))

# "The purple book is the third from the left"
problem.addConstraint(lambda purple: purple == 3, ("purple",))

# Solve for valid arrangements
solutions = problem.getSolutions()

# Determine the leftmost book (position 1)
choices = {
    "A": "blue",
    "B": "purple",
    "C": "yellow",
    "D": "red",
    "E": "gray"
}

# Find and print the correct choice
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 1:
            print(letter)