from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 5)
birds = ["blue jay", "cardinal", "hawk", "hummingbird", "quail"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints
# All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# The quail is to the left of the blue jay
problem.addConstraint(lambda quail, blue_jay: quail < blue_jay, ["quail", "blue jay"])

# The cardinal is the third from the left
problem.addConstraint(lambda cardinal: cardinal == 3, ["cardinal"])

# The quail is the second from the left
problem.addConstraint(lambda quail: quail == 2, ["quail"])

# The blue jay is to the left of the hummingbird
problem.addConstraint(lambda blue_jay, hummingbird: blue_jay < hummingbird, ["blue jay", "hummingbird"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names
choices = {
    "A": "blue jay",
    "B": "cardinal",
    "C": "hawk",
    "D": "hummingbird",
    "E": "quail"
}

# Find the bird at position 1 (leftmost) and print corresponding choice letter
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 1:
            print(letter)