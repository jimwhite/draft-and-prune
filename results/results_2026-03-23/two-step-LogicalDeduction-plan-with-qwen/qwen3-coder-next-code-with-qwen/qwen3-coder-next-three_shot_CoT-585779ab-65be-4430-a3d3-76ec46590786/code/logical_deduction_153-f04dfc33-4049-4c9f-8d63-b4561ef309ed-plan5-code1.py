from constraint import *

# Initialize the constraint satisfaction problem.
problem = Problem()

# Define the variables (the seven books) and the domain (positions 1 to 7).
books = ["yellow", "red", "gray", "blue", "white", "orange", "purple"]
positions = range(1, 8)
problem.addVariables(books, positions)

# Add constraints based on the puzzle's statements.
# 1. All books must be in unique positions.
problem.addConstraint(AllDifferentConstraint())

# 2. "The red book is the third from the right." → position = 5 (7 - 3 + 1 = 5)
problem.addConstraint(lambda red: red == 5, ["red"])

# 3. "The white book is to the right of the orange book." → white > orange
problem.addConstraint(lambda orange, white: orange < white, ["orange", "white"])

# 4. "The purple book is the third from the left." → position = 3
problem.addConstraint(lambda purple: purple == 3, ["purple"])

# 5. "The yellow book is to the right of the purple book." → yellow > purple (i.e., yellow > 3)
problem.addConstraint(lambda purple, yellow: purple < yellow, ["purple", "yellow"])

# 6. "The blue book is to the right of the red book." → blue > red (i.e., blue > 5)
problem.addConstraint(lambda red, blue: red < blue, ["red", "blue"])

# 7. "The blue book is to the left of the gray book." → blue < gray
problem.addConstraint(lambda blue, gray: blue < gray, ["blue", "gray"])

# Find the solution(s)
solutions = problem.getSolutions()

# The question asks which book is second from the left (position 2).
choices = {
    "A": "yellow",
    "B": "red",
    "C": "gray",
    "D": "blue",
    "E": "white",
    "F": "orange",
    "G": "purple"
}

# Find the book at position 2 and print its corresponding choice letter.
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 2:
            print(letter)