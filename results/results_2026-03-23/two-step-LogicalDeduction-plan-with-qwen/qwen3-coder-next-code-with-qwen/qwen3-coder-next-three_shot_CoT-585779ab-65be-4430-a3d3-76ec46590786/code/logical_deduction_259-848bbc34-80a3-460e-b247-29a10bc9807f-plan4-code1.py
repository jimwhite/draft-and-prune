from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
birds = ["cardinal", "hawk", "hummingbird"]
positions = range(1, 4)
problem.addVariables(birds, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The hummingbird is to the right of the hawk" => hummingbird > hawk
problem.addConstraint(lambda hawk, hummingbird: hummingbird > hawk, ["hawk", "hummingbird"])

# "The cardinal is to the left of the hawk" => cardinal < hawk
problem.addConstraint(lambda cardinal, hawk: cardinal < hawk, ["cardinal", "hawk"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to birds
choices = {
    "A": "cardinal",
    "B": "hawk",
    "C": "hummingbird"
}

# Find which bird is leftmost (position 1)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 1:
            print(letter)