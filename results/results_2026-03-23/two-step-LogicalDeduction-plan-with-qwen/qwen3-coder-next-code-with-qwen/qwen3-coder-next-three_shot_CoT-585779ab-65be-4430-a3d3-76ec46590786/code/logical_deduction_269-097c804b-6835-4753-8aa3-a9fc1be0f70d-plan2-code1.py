from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
golfers = ["mel", "ada", "ana"]
positions = range(1, 4)
problem.addVariables(golfers, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "Mel finished last" -> mel's position = 3
problem.addConstraint(lambda mel: mel == 3, ["mel"])

# "Ana finished second" -> ana's position = 2
problem.addConstraint(lambda ana: ana == 2, ["ana"])

# Solve the problem
solutions = problem.getSolutions()

# Determine the correct answer based on the choices
for solution in solutions:
    # Check each choice
    if solution["mel"] == 2:  # Choice A
        print("A")
    elif solution["ada"] == 2:  # Choice B
        print("B")
    elif solution["ana"] == 2:  # Choice C
        print("C")