from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (books) and domain (positions 1 to 7, where 1=leftmost, 7=rightmost)
books = ["brown", "white", "black", "yellow", "orange", "blue", "green"]
positions = range(1, 8)
problem.addVariables(books, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem statements:
# 1. The yellow book is the rightmost (position 7)
problem.addConstraint(lambda yellow: yellow == 7, ["yellow"])

# 2. The blue book is to the left of the orange book (blue < orange)
problem.addConstraint(lambda blue, orange: blue < orange, ["blue", "orange"])

# 3. The green book is to the right of the white book (white < green)
problem.addConstraint(lambda white, green: white < green, ["white", "green"])

# 4. The blue book is to the right of the green book (green < blue)
problem.addConstraint(lambda green, blue: green < blue, ["green", "blue"])

# 5. The black book is the fourth from the left (position 4)
problem.addConstraint(lambda black: black == 4, ["black"])

# 6. The brown book is the third from the right (position 5, since 7-3+1=5)
problem.addConstraint(lambda brown: brown == 5, ["brown"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to book names (A-G)
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