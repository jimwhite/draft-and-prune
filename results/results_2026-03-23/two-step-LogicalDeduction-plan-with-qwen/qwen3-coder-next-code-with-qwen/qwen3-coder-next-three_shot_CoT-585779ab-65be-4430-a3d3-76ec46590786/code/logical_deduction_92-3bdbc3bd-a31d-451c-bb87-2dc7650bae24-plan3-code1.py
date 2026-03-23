from constraint import *

# Initialize the constraint satisfaction problem.
problem = Problem()

# Define the variables (the five books) and the domain (their positions on the shelf).
# Positions: 1 = leftmost, 5 = rightmost
books = ["white", "green", "brown", "gray", "orange"]
positions = range(1, 6)
problem.addVariables(books, positions)

# Add constraints based on the puzzle's statements.
# 1. All books must be in a unique position.
problem.addConstraint(AllDifferentConstraint())

# 2. "The gray book is to the right of the orange book."
problem.addConstraint(lambda gray, orange: gray > orange, ("gray", "orange"))

# 3. "The green book is the second from the right."
problem.addConstraint(lambda green: green == 4, ("green",))

# 4. "The brown book is to the right of the white book."
problem.addConstraint(lambda brown, white: brown > white, ("brown", "white"))

# 5. "The brown book is to the left of the orange book."
problem.addConstraint(lambda brown, orange: brown < orange, ("brown", "orange"))

# Find the unique solution to the problem.
solutions = problem.getSolutions()

# The question asks which book is the "second from the left" (position 2).
choices = {
    "A": "white",
    "B": "green",
    "C": "brown",
    "D": "gray",
    "E": "orange"
}

# Check the solution to find which book is at position 2 and print its corresponding letter.
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 2:
            print(letter)