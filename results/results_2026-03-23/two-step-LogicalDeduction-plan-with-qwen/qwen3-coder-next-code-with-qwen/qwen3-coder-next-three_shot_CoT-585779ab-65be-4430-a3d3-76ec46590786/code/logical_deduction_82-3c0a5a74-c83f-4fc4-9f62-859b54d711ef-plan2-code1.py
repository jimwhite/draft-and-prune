from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
books = ["blue", "purple", "yellow", "red", "gray"]
positions = range(1, 6)
problem.addVariables(books, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The yellow book is to the right of the gray book" -> yellow > gray
problem.addConstraint(lambda yellow, gray: yellow > gray, ("yellow", "gray"))

# "The purple book is to the left of the gray book" -> purple < gray
problem.addConstraint(lambda purple, gray: purple < gray, ("purple", "gray"))

# "The red book is to the right of the blue book" -> red > blue
problem.addConstraint(lambda red, blue: red > blue, ("red", "blue"))

# "The purple book is the third from the left" -> purple == 3
problem.addConstraint(lambda purple: purple == 3, ("purple",))

# Solve the problem
solutions = problem.getSolutions()

# Map choices to book names
choices = {
    "A": "blue",
    "B": "purple",
    "C": "yellow",
    "D": "red",
    "E": "gray"
}

# Find which book is at position 2 (second from the left)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 2:
            print(letter)