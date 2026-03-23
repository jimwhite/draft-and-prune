from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
books = ["gray", "red", "yellow", "blue", "orange"]
positions = range(1, 6)
problem.addVariables(books, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# Gray is to the right of yellow: gray > yellow
problem.addConstraint(lambda gray, yellow: gray > yellow, ("gray", "yellow"))

# Orange is to the right of red: orange > red
problem.addConstraint(lambda orange, red: orange > red, ("orange", "red"))

# Blue is the rightmost: blue == 5
problem.addConstraint(lambda blue: blue == 5, ("blue",))

# Gray is to the left of red: gray < red
problem.addConstraint(lambda gray, red: gray < red, ("gray", "red"))

# Solve the problem
solutions = problem.getSolutions()

# Check which book is at position 5 (rightmost)
for solution in solutions:
    for letter, book_name in [("A", "gray"), ("B", "red"), ("C", "yellow"), ("D", "blue"), ("E", "orange")]:
        if solution[book_name] == 5:
            print(letter)