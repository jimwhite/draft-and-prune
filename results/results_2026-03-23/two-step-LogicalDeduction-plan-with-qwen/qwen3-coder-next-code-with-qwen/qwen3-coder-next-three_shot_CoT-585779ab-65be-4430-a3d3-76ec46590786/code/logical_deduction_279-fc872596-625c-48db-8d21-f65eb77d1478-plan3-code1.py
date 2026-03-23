from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (the three birds) and domain (positions 1 to 3)
birds = ["blue jay", "cardinal", "quail"]
positions = range(1, 4)
problem.addVariables(birds, positions)

# Add constraints
# All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# "The quail is to the right of the blue jay" → blue_jay < quail
problem.addConstraint(lambda blue_jay, quail: blue_jay < quail, ["blue jay", "quail"])

# "The cardinal is to the right of the quail" → quail < cardinal
problem.addConstraint(lambda quail, cardinal: quail < cardinal, ["quail", "cardinal"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names
choices = {
    "A": "blue jay",
    "B": "cardinal",
    "C": "quail"
}

# Find which bird is in position 2 (second from the left)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 2:
            print(letter)