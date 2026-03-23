from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
birds = ["blue jay", "cardinal", "quail"]
positions = range(1, 4)
problem.addVariables(birds, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The quail is to the right of the blue jay" → blue_jay < quail
problem.addConstraint(lambda blue_jay, quail: blue_jay < quail, ["blue jay", "quail"])

# "The cardinal is to the right of the quail" → quail < cardinal
problem.addConstraint(lambda quail, cardinal: quail < cardinal, ["quail", "cardinal"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to birds
choices = {
    "A": "blue jay",
    "B": "cardinal",
    "C": "quail"
}

# Find which bird is at position 1 (leftmost)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 1:
            print(letter)