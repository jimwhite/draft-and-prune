from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7)
birds = ["blue jay", "owl", "falcon", "hawk", "raven", "crow", "hummingbird"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add deterministic constraints
problem.addConstraint(lambda falcon: falcon == 2, ["falcon"])
problem.addConstraint(lambda crow: crow == 7, ["crow"])

# Add relational constraints
problem.addConstraint(lambda hummingbird, blue_jay: hummingbird > blue_jay, ["hummingbird", "blue jay"])
problem.addConstraint(lambda hawk, hummingbird: hawk > hummingbird, ["hawk", "hummingbird"])
problem.addConstraint(lambda blue_jay, owl: blue_jay > owl, ["blue jay", "owl"])
problem.addConstraint(lambda raven: raven < 2, ["raven"])  # raven must be left of falcon (position 2), so raven == 1

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names
choices = {
    "A": "blue jay",
    "B": "owl",
    "C": "falcon",
    "D": "hawk",
    "E": "raven",
    "F": "crow",
    "G": "hummingbird"
}

# Find the bird at position 6 (second from the right)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 6:
            print(letter)