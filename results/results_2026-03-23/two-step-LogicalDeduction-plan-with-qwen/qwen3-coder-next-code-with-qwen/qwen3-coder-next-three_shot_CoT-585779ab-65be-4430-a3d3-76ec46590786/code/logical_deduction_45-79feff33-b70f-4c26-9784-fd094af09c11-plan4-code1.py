from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 5, left to right)
birds = ["cardinal", "robin", "blue jay", "quail", "raven"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints
# All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# "The cardinal is the leftmost" → position 1
problem.addConstraint(lambda cardinal: cardinal == 1, ["cardinal"])

# "The blue jay is the third from the left" → position 3
problem.addConstraint(lambda blue_jay: blue_jay == 3, ["blue jay"])

# "The raven is to the right of the blue jay" → blue_jay < raven
problem.addConstraint(lambda blue_jay, raven: blue_jay < raven, ["blue jay", "raven"])

# "The robin is to the right of the raven" → raven < robin
problem.addConstraint(lambda raven, robin: raven < robin, ["raven", "robin"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to birds (second from the right is position 4)
choices = {
    "A": "cardinal",
    "B": "robin",
    "C": "blue jay",
    "D": "quail",
    "E": "raven"
}

# Find which bird is at position 4 (second from the right)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 4:
            print(letter)