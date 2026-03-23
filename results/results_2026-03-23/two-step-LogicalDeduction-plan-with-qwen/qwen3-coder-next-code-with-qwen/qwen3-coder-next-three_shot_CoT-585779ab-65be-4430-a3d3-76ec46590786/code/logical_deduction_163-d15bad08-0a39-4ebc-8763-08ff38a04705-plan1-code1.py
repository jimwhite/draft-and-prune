from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (the seven birds)
birds = ["raven", "cardinal", "falcon", "owl", "blue_jay", "quail", "robin"]

# Define domain: positions 1 to 7 (1 = leftmost, 7 = rightmost)
positions = range(1, 8)

# Add variables with their domain
problem.addVariables(birds, positions)

# Add constraint that all birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "The owl is the second from the right" → position 6
problem.addConstraint(lambda owl: owl == 6, ["owl"])

# "The cardinal is the fourth from the left" → position 4
problem.addConstraint(lambda cardinal: cardinal == 4, ["cardinal"])

# "The falcon is to the left of the blue jay" → falcon < blue_jay
problem.addConstraint(lambda falcon, blue_jay: falcon < blue_jay, ["falcon", "blue_jay"])

# "The quail is to the left of the falcon" → quail < falcon
problem.addConstraint(lambda quail, falcon: quail < falcon, ["quail", "falcon"])

# "The raven is the second from the left" → position 2
problem.addConstraint(lambda raven: raven == 2, ["raven"])

# "The robin is to the left of the quail" → robin < quail
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