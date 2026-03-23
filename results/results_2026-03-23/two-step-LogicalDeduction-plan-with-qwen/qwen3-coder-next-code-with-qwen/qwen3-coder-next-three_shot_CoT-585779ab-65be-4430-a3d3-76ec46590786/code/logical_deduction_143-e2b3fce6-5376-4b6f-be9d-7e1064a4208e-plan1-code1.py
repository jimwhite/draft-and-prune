from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7)
birds = ["quail", "raven", "hummingbird", "robin", "falcon", "owl", "blue jay"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "The blue jay is to the left of the falcon"
problem.addConstraint(lambda blue_jay, falcon: blue_jay < falcon, ["blue jay", "falcon"])

# "The blue jay is the second from the right" (position 6)
problem.addConstraint(lambda blue_jay: blue_jay == 6, ["blue jay"])

# "The raven is to the left of the robin"
problem.addConstraint(lambda raven, robin: raven < robin, ["raven", "robin"])

# "The owl is the third from the right" (position 5)
problem.addConstraint(lambda owl: owl == 5, ["owl"])

# "The hummingbird is to the left of the quail"
problem.addConstraint(lambda hummingbird, quail: hummingbird < quail, ["hummingbird", "quail"])

# "The raven is the third from the left" (position 3)
problem.addConstraint(lambda raven: raven == 3, ["raven"])

# Solve the problem
solutions = problem.getSolutions()

# Map birds to choice letters
choices_map = {
    "quail": "A",
    "raven": "B",
    "hummingbird": "C",
    "robin": "D",
    "falcon": "E",
    "owl": "F",
    "blue jay": "G"
}

# Find the bird at position 1 (leftmost)
for solution in solutions:
    for bird, pos in solution.items():
        if pos == 1:
            print(choices_map[bird])