from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (the seven books) and domain (positions 1 to 7)
books = ["brown", "white", "black", "yellow", "orange", "blue", "green"]
positions = range(1, 8)
problem.addVariables(books, positions)

# Add constraints based on the problem description
# 1. All books must be in different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The yellow book is the rightmost" → position 7
problem.addConstraint(lambda yellow: yellow == 7, ["yellow"])

# 3. "The blue book is to the left of the orange book" → blue < orange
problem.addConstraint(lambda blue, orange: blue < orange, ["blue", "orange"])

# 4. "The green book is to the right of the white book" → white < green
problem.addConstraint(lambda white, green: white < green, ["white", "green"])

# 5. "The blue book is to the right of the green book" → green < blue
problem.addConstraint(lambda green, blue: green < blue, ["green", "blue"])

# 6. "The black book is the fourth from the left" → position 4
problem.addConstraint(lambda black: black == 4, ["black"])

# 7. "The brown book is the third from the right" → position 5 (since 7=rightmost, 6=second right, 5=third right)
problem.addConstraint(lambda brown: brown == 5, ["brown"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to book names
choices = {
    "A": "brown",
    "B": "white",
    "C": "black",
    "D": "yellow",
    "E": "orange",
    "F": "blue",
    "G": "green"
}

# Find which book is at position 6 (second from the right)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 6:
            print(letter)