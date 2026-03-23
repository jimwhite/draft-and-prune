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
problem.addConstraint(lambda blue_jay: blue_jay == 5, ["blue jay"])

# "The robin is to the right of the falcon"
problem.addConstraint(lambda falcon, robin: falcon < robin, ["falcon", "robin"])

# "The cardinal is to the left of the hawk"
problem.addConstraint(lambda cardinal, hawk: cardinal < hawk, ["cardinal", "hawk"])

# "The falcon is to the right of the hawk"
problem.addConstraint(lambda hawk, falcon: hawk < falcon, ["hawk", "falcon"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to birds
choices = {
    "A": "blue jay",
    "B": "robin",
    "C": "cardinal",
    "D": "hawk",
    "E": "falcon"
}

# Find which bird is in position 4 (second from the right)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 4:
            print(letter)