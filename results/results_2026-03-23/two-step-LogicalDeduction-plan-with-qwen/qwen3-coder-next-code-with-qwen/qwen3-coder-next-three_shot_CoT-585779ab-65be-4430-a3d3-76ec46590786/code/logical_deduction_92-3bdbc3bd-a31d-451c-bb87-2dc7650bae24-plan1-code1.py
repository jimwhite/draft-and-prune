from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
books = ["white", "green", "brown", "gray", "orange"]
positions = range(1, 6)
problem.addVariables(books, positions)

# Add constraints
# All books must be in different positions
problem.addConstraint(AllDifferentConstraint())

# "The gray book is to the right of the orange book" → gray > orange
problem.addConstraint(lambda gray, orange: gray > orange, ("gray", "orange"))

# "The green book is the second from the right" → green == 4
problem.addConstraint(lambda green: green == 4, ("green",))

# "The brown book is to the right of the white book" → brown > white
problem.addConstraint(lambda brown, white: brown > white, ("brown", "white"))

# "The brown book is to the left of the orange book" → brown < orange
problem.addConstraint(lambda brown, orange: brown < orange, ("brown", "orange"))

# Solve the problem
solutions = problem.getSolutions()

# Map choices to book names
choices = {
    "A": "white",
    "B": "green",
    "C": "brown",
    "D": "gray",
    "E": "orange"
}

# Find which book is at position 2 (second from the left)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 2:
            print(letter)