from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 3, where 1 = first, 3 = last)
golfers = ["Mel", "Ada", "Ana"]
positions = range(1, 4)
problem.addVariables(golfers, positions)

# Add constraint: all golfers must have different positions
problem.addConstraint(AllDifferentConstraint())

# "Mel finished last" → Mel's position is 3
problem.addConstraint(lambda Mel: Mel == 3, ["Mel"])

# "Ana finished second" → Ana's position is 2
problem.addConstraint(lambda Ana: Ana == 2, ["Ana"])

# Solve the problem
solutions = problem.getSolutions()

# Determine which choice is true based on the solution
# Choices:
# A) Mel finished second. → check if Mel == 2
# B) Ada finished second. → check if Ada == 2
# C) Ana finished second. → check if Ana == 2

for solution in solutions:
    # Since we know the constraints fix Mel=3 and Ana=2, Ada must be 1
    # But we'll check the choices directly from the solution
    if solution["Mel"] == 2:
        print("A")
    elif solution["Ada"] == 2:
        print("B")
    elif solution["Ana"] == 2:
        print("C")