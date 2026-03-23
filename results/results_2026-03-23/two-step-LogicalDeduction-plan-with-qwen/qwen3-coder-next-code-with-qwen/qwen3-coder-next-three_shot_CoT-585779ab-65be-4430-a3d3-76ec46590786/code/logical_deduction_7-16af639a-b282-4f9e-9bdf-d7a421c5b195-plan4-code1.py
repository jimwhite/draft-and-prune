from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
birds = ["cardinal", "robin", "blue_jay", "quail", "raven"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The cardinal is the leftmost"
problem.addConstraint(lambda cardinal: cardinal == 1, ["cardinal"])

# "The blue jay is the third from the left"
problem.addConstraint(lambda blue_jay: blue_jay == 3, ["blue_jay"])

# "The raven is to the right of the blue jay"
problem.addConstraint(lambda blue_jay, raven: blue_jay < raven, ["blue_jay", "raven"])

# "The robin is to the right of the raven"
problem.addConstraint(lambda raven, robin: raven < robin, ["raven", "robin"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to bird names
choices = {
    "A": "cardinal",
    "B": "robin",
    "C": "blue_jay",
    "D": "quail",
    "E": "raven"
}

# Find which bird is at position 2 (second from the left)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 2:
            print(letter)