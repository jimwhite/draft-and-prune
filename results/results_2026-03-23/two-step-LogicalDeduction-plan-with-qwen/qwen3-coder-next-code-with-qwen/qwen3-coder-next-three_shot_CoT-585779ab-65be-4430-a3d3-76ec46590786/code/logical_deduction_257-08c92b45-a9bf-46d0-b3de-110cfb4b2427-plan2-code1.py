from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables and domain
books = ["yellow", "green", "red"]
positions = [1, 2, 3]
problem.addVariables(books, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The red book is to the left of the green book" => red < green
problem.addConstraint(lambda red, green: red < green, ("red", "green"))

# "The yellow book is to the left of the red book" => yellow < red
problem.addConstraint(lambda yellow, red: yellow < red, ("yellow", "red"))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to book names
choices = {
    "A": "yellow",
    "B": "green",
    "C": "red"
}

# Find which book is in position 2 (second from the left)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 2:
            print(letter)