from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
vehicles = ["sedan", "minivan", "motorcyle"]
ranks = range(1, 4)  # 1=oldest, 2=second-newest, 3=newest
problem.addVariables(vehicles, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The motorcyle is the second-newest"
problem.addConstraint(lambda motorcyle: motorcyle == 2, ["motorcyle"])

# "The minivan is newer than the motorcyle"
problem.addConstraint(lambda minivan, motorcyle: minivan > motorcyle, ["minivan", "motorcyle"])

# Solve the problem
solutions = problem.getSolutions()

# Since there's only one solution, get it directly
solution = solutions[0]

# Check which choice is true
if solution["motorcyle"] == 2:
    print("C")