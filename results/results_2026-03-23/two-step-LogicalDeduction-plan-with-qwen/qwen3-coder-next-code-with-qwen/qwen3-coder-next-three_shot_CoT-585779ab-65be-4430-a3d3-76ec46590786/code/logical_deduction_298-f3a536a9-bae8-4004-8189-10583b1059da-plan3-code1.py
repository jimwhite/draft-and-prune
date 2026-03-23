from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
books = ["white", "green", "orange"]
positions = range(1, 4)
problem.addVariables(books, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The green book is to the right of the white book" => green > white
problem.addConstraint(lambda white, green: green > white, ["white", "green"])

# "The orange book is the rightmost" => orange == 3
problem.addConstraint(lambda orange: orange == 3, ["orange"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to book names
choices = {
    "A": "white",
    "B": "green",
    "C": "orange"
}

# Find which book is leftmost (position 1)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 1:
            print(letter)