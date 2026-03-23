from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define the seven books as variables
books = ["purple", "brown", "red", "blue", "gray", "black", "green"]

# Define the domain as positions 1 to 7 (1 = leftmost, 7 = rightmost)
positions = range(1, 8)
problem.addVariables(books, positions)

# Add the all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# 1. "The brown book is to the left of the green book" → brown < green
problem.addConstraint(lambda brown, green: brown < green, ["brown", "green"])

# 2. "The gray book is the second from the left" → gray == 2
problem.addConstraint(lambda gray: gray == 2, ["gray"])

# 3. "The black book is to the left of the gray book" → black < gray
problem.addConstraint(lambda black, gray: black < gray, ["black", "gray"])

# 4. "The blue book is to the left of the red book" → blue < red
problem.addConstraint(lambda blue, red: blue < red, ["blue", "red"])

# 5. "The blue book is the second from the right" → blue == 6
problem.addConstraint(lambda blue: blue == 6, ["blue"])

# 6. "The green book is to the left of the purple book" → green < purple
problem.addConstraint(lambda green, purple: green < purple, ["green", "purple"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to book names
choices = {
    "A": "purple",
    "B": "brown",
    "C": "red",
    "D": "blue",
    "E": "gray",
    "F": "black",
    "G": "green"
}

# Find which book is in position 4 (fourth from the left)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 4:
            print(letter)