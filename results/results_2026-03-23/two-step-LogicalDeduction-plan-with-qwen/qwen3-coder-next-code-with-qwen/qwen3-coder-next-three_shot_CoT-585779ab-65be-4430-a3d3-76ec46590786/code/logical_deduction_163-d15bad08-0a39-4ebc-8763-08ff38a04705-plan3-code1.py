from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7)
birds = ["raven", "cardinal", "falcon", "owl", "blue jay", "quail", "robin"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "The owl is the second from the right" → position 6
problem.addConstraint(lambda owl: owl == 6, ["owl"])

# "The cardinal is the fourth from the left" → position 4
problem.addConstraint(lambda cardinal: cardinal == 4, ["cardinal"])

# "The falcon is to the left of the blue jay" → falcon < blue jay
problem.addConstraint(lambda falcon, blue_jay: falcon < blue_jay, ["falcon", "blue jay"])

# "The quail is to the left of the falcon" → quail < falcon
problem.addConstraint(lambda quail, falcon: quail < falcon, ["quail", "falcon"])

# "The raven is the second from the left" → position 2
problem.addConstraint(lambda raven: raven == 2, ["raven"])

# "The robin is to the left of the quail" → robin < quail
problem.addConstraint(lambda robin, quail: robin < quail, ["robin", "quail"])

# Solve the problem
solutions = problem.getSolutions()

# Get the first (and only) solution
solution = solutions[0]

# Map choice letters to bird names
choices = {
    'A': "raven",
    'B': "cardinal",
    'C': "falcon",
    'D': "owl",
    'E': "blue jay",
    'F': "quail",
    'G': "robin"
}

# Find which bird is at position 1 (leftmost)
for letter, bird_name in choices.items():
    if solution[bird_name] == 1:
        print(letter)