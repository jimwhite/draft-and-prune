from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (books) and domain (positions 1 to 5, where 1=leftmost, 5=rightmost)
books = ["black", "brown", "yellow", "orange", "red"]
positions = range(1, 6)
problem.addVariables(books, positions)

# Add constraints
# All books must be in different positions
problem.addConstraint(AllDifferentConstraint())

# "The black book is to the left of the yellow book"
problem.addConstraint(lambda black, yellow: black < yellow, ("black", "yellow"))

# "The red book is the third from the left"
problem.addConstraint(lambda red: red == 3, ("red",))

# "The brown book is the second from the left"
problem.addConstraint(lambda brown: brown == 2, ("brown",))

# "The yellow book is to the left of the orange book"
problem.addConstraint(lambda yellow, orange: yellow < orange, ("yellow", "orange"))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to book names
choices = {
    "A": "black",
    "B": "brown",
    "C": "yellow",
    "D": "orange",
    "E": "red"
}

# Find which book is at position 5 (rightmost)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 5:
            print(letter)