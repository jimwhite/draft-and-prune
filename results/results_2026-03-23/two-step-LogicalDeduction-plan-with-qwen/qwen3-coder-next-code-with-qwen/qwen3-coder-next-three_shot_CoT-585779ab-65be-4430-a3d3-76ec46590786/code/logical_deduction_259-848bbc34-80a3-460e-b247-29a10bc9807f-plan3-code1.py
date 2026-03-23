from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (the three birds) and domain (positions 1 to 3)
birds = ["cardinal", "hawk", "hummingbird"]
positions = range(1, 4)
problem.addVariables(birds, positions)

# Add constraints based on the statements
# 1. All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The hummingbird is to the right of the hawk" => hummingbird > hawk
problem.addConstraint(lambda hawk, hummingbird: hummingbird > hawk, ("hawk", "hummingbird"))

# 3. "The cardinal is to the left of the hawk" => cardinal < hawk
problem.addConstraint(lambda cardinal, hawk: cardinal < hawk, ("cardinal", "hawk"))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names
choices = {
    "A": "cardinal",
    "B": "hawk",
    "C": "hummingbird"
}

# Find which bird is at position 1 (leftmost) and print the corresponding letter
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 1:
            print(letter)