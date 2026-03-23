from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (the seven books) and domain (positions 1 to 7)
books = ["green", "brown", "white", "black", "orange", "purple", "yellow"]
positions = range(1, 8)
problem.addVariables(books, positions)

# Add constraints based on the problem description
# 1. All books must be in different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The purple book is to the left of the yellow book."
problem.addConstraint(lambda purple, yellow: purple < yellow, ("purple", "yellow"))

# 3. "The green book is to the left of the white book."
problem.addConstraint(lambda green, white: green < white, ("green", "white"))

# 4. "The brown book is to the right of the yellow book."
problem.addConstraint(lambda yellow, brown: yellow < brown, ("yellow", "brown"))

# 5. "The white book is the fourth from the left."
problem.addConstraint(lambda white: white == 4, ("white",))

# 6. "The green book is to the right of the orange book."
problem.addConstraint(lambda orange, green: orange < green, ("orange", "green"))

# 7. "The black book is the second from the left."
problem.addConstraint(lambda black: black == 2, ("black",))

# Solve for all valid arrangements
solutions = problem.getSolutions()

# Map choice letters to book names
choices = {
    "A": "green",
    "B": "brown",
    "C": "white",
    "D": "black",
    "E": "orange",
    "F": "purple",
    "G": "yellow"
}

# Find which book is at position 3 (third from the left)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 3:
            print(letter)