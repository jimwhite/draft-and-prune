from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 5)
birds = ["cardinal", "robin", "bluejay", "quail", "raven"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints
# All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# "The robin is to the right of the raven" → robin > raven
problem.addConstraint(lambda robin, raven: robin > raven, ["robin", "raven"])

# "The cardinal is the leftmost" → cardinal == 1
problem.addConstraint(lambda cardinal: cardinal == 1, ["cardinal"])

# "The raven is to the right of the blue jay" → raven > bluejay
problem.addConstraint(lambda raven, bluejay: raven > bluejay, ["raven", "bluejay"])

# "The blue jay is the third from the left" → bluejay == 3
problem.addConstraint(lambda bluejay: bluejay == 3, ["bluejay"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to bird names
choices = {
    "A": "cardinal",
    "B": "robin",
    "C": "bluejay",
    "D": "quail",
    "E": "raven"
}

# Find which bird is at position 2 (second from the left)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 2:
            print(letter)