from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (the seven books)
books = ["black", "yellow", "white", "gray", "purple", "orange", "green"]

# Define domain (positions 1 to 7, where 1 is leftmost and 7 is rightmost)
positions = range(1, 8)

# Add variables with their domain
problem.addVariables(books, positions)

# Add AllDifferent constraint to ensure each book is in a unique position
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem statements:
# 1. "The green book is to the left of the gray book" → green < gray
problem.addConstraint(lambda green, gray: green < gray, ("green", "gray"))

# 2. "The gray book is the third from the right" → position = 7 - 3 + 1 = 5
problem.addConstraint(lambda gray: gray == 5, ("gray",))

# 3. "The white book is the rightmost" → position = 7
problem.addConstraint(lambda white: white == 7, ("white",))

# 4. "The orange book is the second from the left" → position = 2
problem.addConstraint(lambda orange: orange == 2, ("orange",))

# 5. "The black book is to the right of the yellow book" → yellow < black
problem.addConstraint(lambda yellow, black: yellow < black, ("yellow", "black"))

# 6. "The black book is the third from the left" → position = 3
problem.addConstraint(lambda black: black == 3, ("black",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to book names
choices = {
    "A": "black",
    "B": "yellow",
    "C": "white",
    "D": "gray",
    "E": "purple",
    "F": "orange",
    "G": "green"
}

# Find which book is at position 4 (fourth from the left)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 4:
            print(letter)