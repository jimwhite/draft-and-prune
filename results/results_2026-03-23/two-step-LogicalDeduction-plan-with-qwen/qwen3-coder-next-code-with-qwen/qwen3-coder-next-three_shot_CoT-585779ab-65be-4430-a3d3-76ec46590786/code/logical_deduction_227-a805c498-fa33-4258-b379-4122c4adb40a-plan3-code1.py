from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (books) and domain (positions 1 to 7, where 1 is leftmost)
books = ["green", "brown", "white", "black", "orange", "purple", "yellow"]
positions = range(1, 8)
problem.addVariables(books, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# 1. "The purple book is to the left of the yellow book" → purple < yellow
problem.addConstraint(lambda purple, yellow: purple < yellow, ("purple", "yellow"))

# 2. "The green book is to the left of the white book" → green < white
problem.addConstraint(lambda green, white: green < white, ("green", "white"))

# 3. "The brown book is to the right of the yellow book" → yellow < brown
problem.addConstraint(lambda yellow, brown: yellow < brown, ("yellow", "brown"))

# 4. "The white book is the fourth from the left" → white == 4
problem.addConstraint(lambda white: white == 4, ("white",))

# 5. "The green book is to the right of the orange book" → orange < green
problem.addConstraint(lambda orange, green: orange < green, ("orange", "green"))

# 6. "The black book is the second from the left" → black == 2
problem.addConstraint(lambda black: black == 2, ("black",))

# Solve the problem
solutions = problem.getSolutions()

# For 7 books, "third from the right" means position: 7 - 3 + 1 = 5
target_position = 5

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

# Find which book is at position 5 and print the corresponding choice letter
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == target_position:
            print(letter)