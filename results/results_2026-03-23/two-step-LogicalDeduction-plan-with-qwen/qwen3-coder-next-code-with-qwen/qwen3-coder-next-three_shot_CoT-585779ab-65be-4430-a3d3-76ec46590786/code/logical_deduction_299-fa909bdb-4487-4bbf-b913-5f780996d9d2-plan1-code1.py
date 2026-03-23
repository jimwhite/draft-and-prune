from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables and domain for three books
books = ["red", "gray", "white"]
positions = range(1, 4)  # 1=leftmost, 2=middle, 3=rightmost
problem.addVariables(books, positions)

# Add constraints based on the statements
# 1. All books must be in different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The white book is to the left of the gray book" => white < gray
problem.addConstraint(lambda white, gray: white < gray, ("white", "gray"))

# 3. "The red book is the second from the left" => red == 2
problem.addConstraint(lambda red: red == 2, ("red",))

# Solve the problem
solutions = problem.getSolutions()

# Determine which book is leftmost (position 1)
leftmost_book = None
for solution in solutions:
    for book, pos in solution.items():
        if pos == 1:
            leftmost_book = book
            break

# Map the leftmost book to the correct choice letter
if leftmost_book == "white":
    print("C")
elif leftmost_book == "gray":
    print("B")
else:  # red cannot be leftmost due to constraint, but included for completeness
    print("A")