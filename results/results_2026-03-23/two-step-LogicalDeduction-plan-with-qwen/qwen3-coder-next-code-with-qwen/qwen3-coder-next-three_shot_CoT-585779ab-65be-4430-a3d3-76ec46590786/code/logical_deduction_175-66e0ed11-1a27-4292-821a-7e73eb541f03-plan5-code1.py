from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (the seven books) and domain (positions 1 to 7)
books = ["red", "purple", "green", "white", "orange", "blue", "gray"]
positions = range(1, 8)
problem.addVariables(books, positions)

# Add constraints
# All books must be in different positions
problem.addConstraint(AllDifferentConstraint())

# "The green book is to the left of the white book."
problem.addConstraint(lambda g, w: g < w, ("green", "white"))

# "The red book is to the left of the purple book."
problem.addConstraint(lambda r, p: r < p, ("red", "purple"))

# "The red book is to the right of the orange book."
problem.addConstraint(lambda o, r: o < r, ("orange", "red"))

# "The gray book is the second from the left."
problem.addConstraint(lambda g: g == 2, ("gray",))

# "The purple book is to the left of the green book."
problem.addConstraint(lambda p, g: p < g, ("purple", "green"))

# "The blue book is the fourth from the left."
problem.addConstraint(lambda b: b == 4, ("blue",))

# Solve for the arrangement
solutions = problem.getSolutions()

# Map choice letters to book names
choices = {
    "A": "red",
    "B": "purple",
    "C": "green",
    "D": "white",
    "E": "orange",
    "F": "blue",
    "G": "gray"
}

# Find which book is in position 6 (second from the right)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 6:
            print(letter)