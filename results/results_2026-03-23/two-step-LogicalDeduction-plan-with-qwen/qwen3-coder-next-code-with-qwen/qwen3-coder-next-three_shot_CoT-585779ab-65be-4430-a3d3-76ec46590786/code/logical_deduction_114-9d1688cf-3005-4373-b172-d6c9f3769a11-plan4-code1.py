from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7)
birds = ["blue jay", "owl", "falcon", "hawk", "raven", "crow", "hummingbird"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Fixed position constraints
# Falcon is second from the left (position 2)
problem.addConstraint(lambda falcon: falcon == 2, ["falcon"])
# Crow is rightmost (position 7)
problem.addConstraint(lambda crow: crow == 7, ["crow"])

# Relative position constraints
# Hummingbird is to the right of blue jay: hummingbird > blue jay
problem.addConstraint(lambda blue_jay, hummingbird: blue_jay < hummingbird, ["blue jay", "hummingbird"])
# Hawk is to the right of hummingbird: hawk > hummingbird
problem.addConstraint(lambda hummingbird, hawk: hummingbird < hawk, ["hummingbird", "hawk"])
# Blue jay is to the right of owl: blue jay > owl
problem.addConstraint(lambda owl, blue_jay: owl < blue_jay, ["owl", "blue jay"])
# Raven is to the left of falcon: raven < falcon (and since falcon=2, raven must be 1)
problem.addConstraint(lambda raven: raven < 2, ["raven"])

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

# Find the bird at position 6 (second from right)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 6:
            print(letter)