from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables (books) and domain (positions 1 to 5, where 1=leftmost, 5=rightmost)
books = ["gray", "red", "purple", "blue", "black"]
positions = range(1, 6)
problem.addVariables(books, positions)

# Add constraints
# All books must be in different positions
problem.addConstraint(AllDifferentConstraint())

# "The red book is to the right of the gray book" → red > gray
problem.addConstraint(lambda gray, red: gray < red, ("gray", "red"))

# "The black book is to the left of the blue book" → black < blue
problem.addConstraint(lambda black, blue: black < blue, ("black", "blue"))

# "The blue book is to the left of the gray book" → blue < gray
problem.addConstraint(lambda blue, gray: blue < gray, ("blue", "gray"))

# "The purple book is the second from the right" → purple == 4
problem.addConstraint(lambda purple: purple == 4, ("purple",))

# Solve the problem
solutions = problem.getSolutions()

# Since all choices refer to who is second from the right (position 4), and we know purple == 4,
# we can directly check which book is at position 4 in the solution
for solution in solutions:
    for letter, book_name in [("A", "gray"), ("B", "red"), ("C", "purple"), ("D", "blue"), ("E", "black")]:
        if solution[book_name] == 4:
            print(letter)