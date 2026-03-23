from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (books) and domain (positions 1 to 7, left to right)
books = ["purple", "green", "white", "gray", "red", "black", "brown"]
positions = range(1, 8)
problem.addVariables(books, positions)

# Add all different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# 1. "The gray book is to the left of the purple book" → gray < purple
problem.addConstraint(lambda gray, purple: gray < purple, ("gray", "purple"))

# 2. "The white book is to the right of the brown book" → brown < white
problem.addConstraint(lambda brown, white: brown < white, ("brown", "white"))

# 3. "The black book is the third from the right" → position = 7 - 3 + 1 = 5
problem.addConstraint(lambda black: black == 5, ("black",))

# 4. "The purple book is to the left of the white book" → purple < white
problem.addConstraint(lambda purple, white: purple < white, ("purple", "white"))

# 5. "The white book is the second from the right" → position = 7 - 2 + 1 = 6
problem.addConstraint(lambda white: white == 6, ("white",))

# 6. "The gray book is the third from the left" → position = 3
problem.addConstraint(lambda gray: gray == 3, ("gray",))

# 7. "The brown book is to the right of the green book" → green < brown
problem.addConstraint(lambda green, brown: green < brown, ("green", "brown"))

# Solve the problem
solutions = problem.getSolutions()

# The question asks which book is second from the right (position 6)
choices = {
    "A": "purple",
    "B": "green",
    "C": "white",
    "D": "gray",
    "E": "red",
    "F": "black",
    "G": "brown"
}

# Find which book is at position 6 and print the corresponding letter
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 6:
            print(letter)