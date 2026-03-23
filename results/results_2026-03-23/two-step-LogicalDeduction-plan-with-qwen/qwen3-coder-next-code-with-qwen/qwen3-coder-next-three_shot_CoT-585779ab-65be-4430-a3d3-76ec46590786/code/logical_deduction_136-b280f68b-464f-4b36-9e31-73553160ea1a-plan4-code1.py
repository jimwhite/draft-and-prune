from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7)
birds = ["bluejay", "owl", "falcon", "hawk", "raven", "crow", "hummingbird"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem description
# The falcon is the second from the left (position 2)
problem.addConstraint(lambda falcon: falcon == 2, ["falcon"])

# The crow is the rightmost (position 7)
problem.addConstraint(lambda crow: crow == 7, ["crow"])

# The hummingbird is to the right of the blue jay (bluejay < hummingbird)
problem.addConstraint(lambda bluejay, hummingbird: bluejay < hummingbird, ["bluejay", "hummingbird"])

# The hawk is to the right of the hummingbird (hummingbird < hawk)
problem.addConstraint(lambda hummingbird, hawk: hummingbird < hawk, ["hummingbird", "hawk"])

# The blue jay is to the right of the owl (owl < bluejay)
problem.addConstraint(lambda owl, bluejay: owl < bluejay, ["owl", "bluejay"])

# The raven is to the left of the falcon (raven < falcon)
problem.addConstraint(lambda raven, falcon: raven < falcon, ["raven", "falcon"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to bird names
choices = {
    "A": "bluejay",
    "B": "owl",
    "C": "falcon",
    "D": "hawk",
    "E": "raven",
    "F": "crow",
    "G": "hummingbird"
}

# Find the bird at position 1 (leftmost) and print corresponding choice letter
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 1:
            print(letter)