from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (books) and domain (positions 1 to 7)
books = ["yellow", "red", "gray", "blue", "white", "orange", "purple"]
positions = range(1, 8)
problem.addVariables(books, positions)

# Add AllDifferent constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "The red book is the third from the right" → position 5 (7 - 3 + 1 = 5)
problem.addConstraint(lambda r: r == 5, ["red"])

# "The white book is to the right of the orange book"
problem.addConstraint(lambda w, o: w > o, ["white", "orange"])

# "The purple book is the third from the left" → position 3
problem.addConstraint(lambda p: p == 3, ["purple"])

# "The yellow book is to the right of the purple book"
problem.addConstraint(lambda y, p: y > p, ["yellow", "purple"])

# "The blue book is to the right of the red book"
problem.addConstraint(lambda b, r: b > r, ["blue", "red"])

# "The blue book is to the left of the gray book"
problem.addConstraint(lambda b, g: b < g, ["blue", "gray"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to book names
choices = {
    "A": "yellow",
    "B": "red",
    "C": "gray",
    "D": "blue",
    "E": "white",
    "F": "orange",
    "G": "purple"
}

# Find which book is in position 2 (second from the left)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 2:
            print(letter)