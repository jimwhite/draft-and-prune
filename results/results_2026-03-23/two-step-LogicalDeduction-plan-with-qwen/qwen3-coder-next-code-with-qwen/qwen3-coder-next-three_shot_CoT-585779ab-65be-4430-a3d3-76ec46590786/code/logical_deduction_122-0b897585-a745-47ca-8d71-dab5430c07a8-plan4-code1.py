from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (the seven birds) and domain (positions 1 to 7)
birds = ["hawk", "crow", "owl", "raven", "falcon", "quail", "hummingbird"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem description:
# 1. "The hummingbird is the second from the left"
problem.addConstraint(lambda hummingbird: hummingbird == 2, ["hummingbird"])

# 2. "The raven is the fourth from the left"
problem.addConstraint(lambda raven: raven == 4, ["raven"])

# 3. "The raven is to the right of the hawk"
problem.addConstraint(lambda hawk, raven: hawk < raven, ["hawk", "raven"])

# 4. "The owl is to the right of the crow"
problem.addConstraint(lambda crow, owl: crow < owl, ["crow", "owl"])

# 5. "The falcon is the rightmost"
problem.addConstraint(lambda falcon: falcon == 7, ["falcon"])

# 6. "The hawk is to the right of the hummingbird"
problem.addConstraint(lambda hummingbird, hawk: hummingbird < hawk, ["hummingbird", "hawk"])

# 7. "The quail is the second from the right"
problem.addConstraint(lambda quail: quail == 6, ["quail"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names for the question about "third from the left"
choices = {
    'A': "hawk",
    'B': "crow",
    'C': "owl",
    'D': "raven",
    'E': "falcon",
    'F': "quail",
    'G': "hummingbird"
}

# Find which bird is at position 3 (third from the left)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 3:
            print(letter)