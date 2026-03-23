from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
books = ["gray", "red", "purple", "blue", "black"]
positions = range(1, 6)
problem.addVariables(books, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The red book is to the right of the gray book" → red > gray
problem.addConstraint(lambda red, gray: red > gray, ("red", "gray"))

# "The black book is to the left of the blue book" → black < blue
problem.addConstraint(lambda black, blue: black < blue, ("black", "blue"))

# "The blue book is to the left of the gray book" → blue < gray
problem.addConstraint(lambda blue, gray: blue < gray, ("blue", "gray"))

# "The purple book is the second from the right" → position 4
problem.addConstraint(lambda purple: purple == 4, ("purple",))

# Solve the problem
solutions = problem.getSolutions()

# Map choices to book names
choices = {
    "A": "gray",
    "B": "red",
    "C": "purple",
    "D": "blue",
    "E": "black"
}

# Find which book is at position 4 (second from the right)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 4:
            print(letter)