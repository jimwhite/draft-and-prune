from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
books = ["yellow", "green", "red"]
positions = range(1, 4)
problem.addVariables(books, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())
problem.addConstraint(lambda red, green: red < green, ["red", "green"])
problem.addConstraint(lambda yellow, red: yellow < red, ["yellow", "red"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to book names
choices = {
    "A": "yellow",
    "B": "green",
    "C": "red"
}

# Find which book is at position 2 (second from the left)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 2:
            print(letter)