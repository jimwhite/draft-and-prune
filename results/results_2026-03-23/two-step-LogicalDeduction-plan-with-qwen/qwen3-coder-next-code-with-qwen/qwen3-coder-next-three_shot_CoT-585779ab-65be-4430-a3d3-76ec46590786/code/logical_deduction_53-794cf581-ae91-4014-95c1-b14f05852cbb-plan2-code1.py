from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
books = ["black", "brown", "yellow", "orange", "red"]
positions = range(1, 6)
problem.addVariables(books, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The black book is to the left of the yellow book"
problem.addConstraint(lambda black, yellow: black < yellow, ("black", "yellow"))

# "The red book is the third from the left"
problem.addConstraint(lambda red: red == 3, ("red",))

# "The brown book is the second from the left"
problem.addConstraint(lambda brown: brown == 2, ("brown",))

# "The yellow book is to the left of the orange book"
problem.addConstraint(lambda yellow, orange: yellow < orange, ("yellow", "orange"))

# Solve the problem
solutions = problem.getSolutions()

# Map books to choice letters
book_to_choice = {
    "black": "A",
    "brown": "B",
    "yellow": "C",
    "orange": "D",
    "red": "E"
}

# Find the rightmost book (position 5) and output its choice letter
for solution in solutions:
    for book, position in solution.items():
        if position == 5:
            print(book_to_choice[book])