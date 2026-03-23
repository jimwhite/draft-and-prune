from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables (books) and domain (positions 1 to 5, where 1 is leftmost, 5 is rightmost)
books = ["gray", "red", "purple", "blue", "black"]
positions = range(1, 6)
problem.addVariables(books, positions)

# Add constraints
# All books must be in different positions
problem.addConstraint(AllDifferentConstraint())

# The red book is to the right of the gray book
problem.addConstraint(lambda red, gray: red > gray, ("red", "gray"))

# The black book is to the left of the blue book
problem.addConstraint(lambda black, blue: black < blue, ("black", "blue"))

# The blue book is to the left of the gray book
problem.addConstraint(lambda blue, gray: blue < gray, ("blue", "gray"))

# The purple book is the second from the right (position 4)
problem.addConstraint(lambda purple: purple == 4, ("purple",))

# Solve the problem
solutions = problem.getSolutions()

# Determine which statement is true (which book is at position 4)
choices = {
    "A": "gray",
    "B": "red",
    "C": "purple",
    "D": "blue",
    "E": "black"
}

# Since we know purple must be at position 4 from the constraint, 
# we can directly check which choice corresponds to purple
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 4:
            print(letter)