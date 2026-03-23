from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (books) and domain (positions 1 to 5, where 1=leftmost, 5=rightmost)
books = ["gray", "red", "purple", "blue", "black"]
positions = range(1, 6)
problem.addVariables(books, positions)

# Add constraints
# All books must be in different positions
problem.addConstraint(AllDifferentConstraint())

# "The red book is to the right of the gray book" → red position > gray position
problem.addConstraint(lambda red, gray: red > gray, ("red", "gray"))

# "The black book is to the left of the blue book" → black position < blue position
problem.addConstraint(lambda black, blue: black < blue, ("black", "blue"))

# "The blue book is to the left of the gray book" → blue position < gray position
problem.addConstraint(lambda blue, gray: blue < gray, ("blue", "gray"))

# "The purple book is the second from the right" → position 4
problem.addConstraint(lambda purple: purple == 4, ("purple",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to book names
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