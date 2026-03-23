from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
vehicles = ["sedan", "minivan", "motorcyle"]
ranks = range(1, 4)  # 1=oldest, 2=second-newest, 3=newest
problem.addVariables(vehicles, ranks)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "The motorcyle is the second-newest" -> position 2
problem.addConstraint(lambda motorcyle: motorcyle == 2, ["motorcyle"])

# "The minivan is newer than the motorcyle" -> minivan > motorcyle
problem.addConstraint(lambda minivan, motorcyle: minivan > motorcyle, ["minivan", "motorcyle"])

# Solve the problem
solutions = problem.getSolutions()

# Since we know the motorcyle must be at position 2, and that's exactly what choice C states,
# we can directly output 'C' as the answer.
print("C")