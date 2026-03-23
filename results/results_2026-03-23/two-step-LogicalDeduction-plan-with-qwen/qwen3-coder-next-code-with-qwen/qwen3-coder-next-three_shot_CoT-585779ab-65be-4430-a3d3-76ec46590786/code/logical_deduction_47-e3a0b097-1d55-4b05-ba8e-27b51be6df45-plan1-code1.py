from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
birds = ["blue jay", "robin", "cardinal", "hawk", "falcon"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The blue jay is the rightmost"
problem.addConstraint(lambda bj: bj == 5, ["blue jay"])

# "The robin is to the right of the falcon"
problem.addConstraint(lambda robin, falcon: robin > falcon, ["robin", "falcon"])

# "The cardinal is to the left of the hawk"
problem.addConstraint(lambda cardinal, hawk: cardinal < hawk, ["cardinal", "hawk"])

# "The falcon is to the right of the hawk"
problem.addConstraint(lambda falcon, hawk: falcon > hawk, ["falcon", "hawk"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to bird names
choices = {
    "A": "blue jay",
    "B": "robin",
    "C": "cardinal",
    "D": "hawk",
    "E": "falcon"
}

# Find which bird is at position 5 (rightmost)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 5:
            print(letter)