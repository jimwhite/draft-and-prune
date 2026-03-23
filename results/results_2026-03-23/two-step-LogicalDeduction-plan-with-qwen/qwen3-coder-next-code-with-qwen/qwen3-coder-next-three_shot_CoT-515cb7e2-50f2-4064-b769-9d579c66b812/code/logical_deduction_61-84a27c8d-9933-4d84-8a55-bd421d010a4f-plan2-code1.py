from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables (books) and domain (positions 1 to 5, where 1=leftmost, 5=rightmost)
books = ["gray", "red", "purple", "blue", "black"]
positions = range(1, 6)
problem.addVariables(books, positions)

# Add constraints based on the problem statements
# 1. All books must be in different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The red book is to the right of the gray book" → red > gray
problem.addConstraint(lambda gray, red: red > gray, ("gray", "red"))

# 3. "The black book is to the left of the blue book" → black < blue
problem.addConstraint(lambda black, blue: black < blue, ("black", "blue"))

# 4. "The blue book is to the left of the gray book" → blue < gray
problem.addConstraint(lambda blue, gray: blue < gray, ("blue", "gray"))

# 5. "The purple book is the second from the right" → purple == 4
problem.addConstraint(lambda purple: purple == 4, ("purple",))

# Solve the problem
solutions = problem.getSolutions()

# The question asks which book is second from the right (position 4)
# According to the constraints, purple must be at position 4
# So option C should be correct: "The purple book is the second from the right."
# Let's verify by checking which book has position 4 in the solution

for solution in solutions:
    # Find which book is at position 4
    for book, pos in solution.items():
        if pos == 4:
            # Map to the correct choice letter
            if book == "purple":
                print("C")
            break