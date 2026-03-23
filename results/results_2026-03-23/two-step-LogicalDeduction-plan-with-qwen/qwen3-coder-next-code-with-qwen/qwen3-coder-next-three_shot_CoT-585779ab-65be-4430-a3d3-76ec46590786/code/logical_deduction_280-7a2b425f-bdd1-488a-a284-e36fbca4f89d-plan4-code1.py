from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables and domain
vehicles = ["sedan", "minivan", "motorcyle"]
positions = range(1, 4)  # 1=oldest, 2=second-newest, 3=newest
problem.addVariables(vehicles, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The motorcyle is the second-newest."
problem.addConstraint(lambda motorcyle: motorcyle == 2, ["motorcyle"])

# "The minivan is newer than the motorcyle."
problem.addConstraint(lambda minivan, motorcyle: minivan > motorcyle, ["minivan", "motorcyle"])

# Solve the problem
solutions = problem.getSolutions()

# Check which choice is true based on the solution
for solution in solutions:
    # According to constraints, motorcyle must be at position 2
    if solution["motorcyle"] == 2:
        print("C")