from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7)
birds = ["hawk", "crow", "owl", "raven", "falcon", "quail", "hummingbird"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add AllDifferentConstraint to ensure each bird is in a unique position
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# 1. "The hummingbird is the second from the left" → hummingbird == 2
problem.addConstraint(lambda hummingbird: hummingbird == 2, ["hummingbird"])

# 2. "The raven is the fourth from the left" → raven == 4
problem.addConstraint(lambda raven: raven == 4, ["raven"])

# 3. "The raven is to the right of the hawk" → hawk < raven (i.e., hawk < 4)
problem.addConstraint(lambda hawk, raven: hawk < raven, ["hawk", "raven"])

# 4. "The owl is to the right of the crow" → crow < owl
problem.addConstraint(lambda crow, owl: crow < owl, ["crow", "owl"])

# 5. "The falcon is the rightmost" → falcon == 7
problem.addConstraint(lambda falcon: falcon == 7, ["falcon"])

# 6. "The hawk is to the right of the hummingbird" → hummingbird < hawk (i.e., 2 < hawk)
problem.addConstraint(lambda hummingbird, hawk: hummingbird < hawk, ["hummingbird", "hawk"])

# 7. "The quail is the second from the right" → quail == 6
problem.addConstraint(lambda quail: quail == 6, ["quail"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names for position 3 (third from the left)
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