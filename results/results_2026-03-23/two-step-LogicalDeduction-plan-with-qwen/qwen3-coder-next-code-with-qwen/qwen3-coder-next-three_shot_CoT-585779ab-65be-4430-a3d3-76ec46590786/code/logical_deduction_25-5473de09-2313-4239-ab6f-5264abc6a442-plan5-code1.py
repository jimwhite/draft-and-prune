from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
books = ["blue", "purple", "yellow", "black", "green"]
positions = range(1, 6)
problem.addVariables(books, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The purple book is the third from the left"
problem.addConstraint(lambda p: p == 3, ["purple"])

# "The green book is to the left of the purple book"
problem.addConstraint(lambda g, p: g < p, ["green", "purple"])

# "The blue book is to the left of the green book"
problem.addConstraint(lambda b, g: b < g, ["blue", "green"])

# "The yellow book is to the left of the black book"
problem.addConstraint(lambda y, k: y < k, ["yellow", "black"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to books
choices = {
    "A": "blue",
    "B": "purple",
    "C": "yellow",
    "D": "black",
    "E": "green"
}

# Find which book is in position 4 (second from the right)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 4:
            print(letter)