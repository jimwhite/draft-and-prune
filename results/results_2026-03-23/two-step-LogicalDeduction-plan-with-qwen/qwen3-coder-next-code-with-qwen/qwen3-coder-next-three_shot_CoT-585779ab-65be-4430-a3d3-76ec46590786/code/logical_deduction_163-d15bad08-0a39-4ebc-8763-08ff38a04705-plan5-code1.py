from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables (the seven birds) and domain (positions 1 to 7)
birds = ["raven", "cardinal", "falcon", "owl", "blue_jay", "quail", "robin"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add constraints based on the problem description
# 1. All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The owl is the second from the right" → position 6
problem.addConstraint(lambda owl: owl == 6, ["owl"])

# 3. "The cardinal is the fourth from the left" → position 4
problem.addConstraint(lambda cardinal: cardinal == 4, ["cardinal"])

# 4. "The falcon is to the left of the blue jay" → falcon < blue_jay
problem.addConstraint(lambda falcon, blue_jay: falcon < blue_jay, ["falcon", "blue_jay"])

# 5. "The quail is to the left of the falcon" → quail < falcon
problem.addConstraint(lambda quail, falcon: quail < falcon, ["quail", "falcon"])

# 6. "The raven is the second from the left" → position 2
problem.addConstraint(lambda raven: raven == 2, ["raven"])

# 7. "The robin is to the left of the quail" → robin < quail
problem.addConstraint(lambda robin, quail: robin < quail, ["robin", "quail"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names
choices = {
    "A": "raven",
    "B": "cardinal",
    "C": "falcon",
    "D": "owl",
    "E": "blue_jay",
    "F": "quail",
    "G": "robin"
}

# Find which bird is at position 1 (leftmost)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 1:
            print(letter)