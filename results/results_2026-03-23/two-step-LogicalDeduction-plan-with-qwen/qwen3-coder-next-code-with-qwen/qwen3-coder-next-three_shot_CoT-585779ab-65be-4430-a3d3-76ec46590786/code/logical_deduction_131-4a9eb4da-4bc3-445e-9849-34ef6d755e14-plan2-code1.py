from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7, where 1 = first, 7 = last)
golfers = ["Joe", "Mel", "Mya", "Eve", "Rob", "Ada", "Dan"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add constraints
# All golfers must have unique positions
problem.addConstraint(AllDifferentConstraint())

# Rob finished first (position 1)
problem.addConstraint(lambda Rob: Rob == 1, ["Rob"])

# Eve finished last (position 7)
problem.addConstraint(lambda Eve: Eve == 7, ["Eve"])

# Joe finished second-to-last (position 6)
problem.addConstraint(lambda Joe: Joe == 6, ["Joe"])

# Mya finished third (position 3)
problem.addConstraint(lambda Mya: Mya == 3, ["Mya"])

# Dan finished above Ada (Dan's position < Ada's position)
problem.addConstraint(lambda Dan, Ada: Dan < Ada, ["Dan", "Ada"])

# Mel finished above Mya (Mel's position < Mya's position)
problem.addConstraint(lambda Mel, Mya: Mel < Mya, ["Mel", "Mya"])

# Solve the problem
solutions = problem.getSolutions()

# The question asks who finished third (position 3)
# According to the constraints, Mya must be in position 3
# Let's verify and map to choices

# Choices mapping: A) Joe, B) Mel, C) Mya, D) Eve, E) Rob, F) Ada, G) Dan
choices = {
    "A": "Joe",
    "B": "Mel",
    "C": "Mya",
    "D": "Eve",
    "E": "Rob",
    "F": "Ada",
    "G": "Dan"
}

# Find who has position 3
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 3:
            print(letter)