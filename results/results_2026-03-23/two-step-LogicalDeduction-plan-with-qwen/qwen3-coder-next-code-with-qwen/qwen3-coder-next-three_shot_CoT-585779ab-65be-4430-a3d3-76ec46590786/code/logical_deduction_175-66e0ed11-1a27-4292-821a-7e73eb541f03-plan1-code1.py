from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (books) and domain (positions 1 to 7)
books = ["red", "purple", "green", "white", "orange", "blue", "gray"]
positions = range(1, 8)
problem.addVariables(books, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# 1. "The green book is to the left of the white book" → green < white
problem.addConstraint(lambda green, white: green < white, ("green", "white"))

# 2. "The red book is to the left of the purple book" → red < purple
problem.addConstraint(lambda red, purple: red < purple, ("red", "purple"))

# 3. "The red book is to the right of the orange book" → orange < red
problem.addConstraint(lambda orange, red: orange < red, ("orange", "red"))

# 4. "The gray book is the second from the left" → gray == 2
problem.addConstraint(lambda gray: gray == 2, ("gray",))

# 5. "The purple book is to the left of the green book" → purple < green
problem.addConstraint(lambda purple, green: purple < green, ("purple", "green"))

# 6. "The blue book is the fourth from the left" → blue == 4
problem.addConstraint(lambda blue: blue == 4, ("blue",))

# Solve the problem
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

# Find which book is at position 6 (second from the right)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 6:
            print(letter)