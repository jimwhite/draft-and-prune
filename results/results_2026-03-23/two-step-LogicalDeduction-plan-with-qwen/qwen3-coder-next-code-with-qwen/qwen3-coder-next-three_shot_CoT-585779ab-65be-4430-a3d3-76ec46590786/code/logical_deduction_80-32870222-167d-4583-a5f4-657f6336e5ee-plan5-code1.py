from constraint import *

# Initialize the constraint satisfaction problem.
problem = Problem()

# Define the variables (the five books) and the domain (their positions on the shelf).
# Positions: 1 = leftmost, 2 = second from left, ..., 5 = rightmost
books = ["yellow", "green", "gray", "blue", "orange"]
positions = range(1, 6)
problem.addVariables(books, positions)

# Add constraints based on the puzzle's statements.
# 1. All books must be in a unique position.
problem.addConstraint(AllDifferentConstraint())

# 2. "The gray book is to the left of the green book."
problem.addConstraint(lambda gray, green: gray < green, ("gray", "green"))

# 3. "The gray book is the second from the right." → position 4
problem.addConstraint(lambda gray: gray == 4, ("gray",))

# 4. "The yellow book is to the right of the orange book."
problem.addConstraint(lambda orange, yellow: orange < yellow, ("orange", "yellow"))

# 5. "The blue book is the second from the left." → position 2
problem.addConstraint(lambda blue: blue == 2, ("blue",))

# Find the unique solution
solutions = problem.getSolutions()

# The question asks which book is third from the left (position 3)
choices = {
    "A": "yellow",
    "B": "green",
    "C": "gray",
    "D": "blue",
    "E": "orange"
}

# Find the book at position 3 and print its corresponding letter
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 3:
            print(letter)