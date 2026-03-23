from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7)
birds = ["hawk", "crow", "owl", "raven", "falcon", "quail", "hummingbird"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add AllDifferent constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "The hummingbird is the second from the left"
problem.addConstraint(lambda hummingbird: hummingbird == 2, ["hummingbird"])

# "The raven is the fourth from the left"
problem.addConstraint(lambda raven: raven == 4, ["raven"])

# "The raven is to the right of the hawk" (hawk < raven)
problem.addConstraint(lambda hawk, raven: hawk < raven, ["hawk", "raven"])

# "The owl is to the right of the crow" (crow < owl)
problem.addConstraint(lambda crow, owl: crow < owl, ["crow", "owl"])

# "The falcon is the rightmost"
problem.addConstraint(lambda falcon: falcon == 7, ["falcon"])

# "The hawk is to the right of the hummingbird" (hummingbird < hawk)
problem.addConstraint(lambda hummingbird, hawk: hummingbird < hawk, ["hummingbird", "hawk"])

# "The quail is the second from the right"
problem.addConstraint(lambda quail: quail == 6, ["quail"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to birds for position 3 (third from left)
choices = {
    "A": "hawk",
    "B": "crow",
    "C": "owl",
    "D": "raven",
    "E": "falcon",
    "F": "quail",
    "G": "hummingbird"
}

# Find which bird is at position 3
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 3:
            print(letter)