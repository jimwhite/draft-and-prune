from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7)
birds = ["blue jay", "owl", "falcon", "hawk", "raven", "crow", "hummingbird"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "The falcon is the second from the left"
problem.addConstraint(lambda falcon: falcon == 2, ["falcon"])

# "The crow is the rightmost"
problem.addConstraint(lambda crow: crow == 7, ["crow"])

# "The hummingbird is to the right of the blue jay"
problem.addConstraint(lambda blue_jay, hummingbird: blue_jay < hummingbird, ["blue jay", "hummingbird"])

# "The hawk is to the right of the hummingbird"
problem.addConstraint(lambda hummingbird, hawk: hummingbird < hawk, ["hummingbird", "hawk"])

# "The blue jay is to the right of the owl"
problem.addConstraint(lambda owl, blue_jay: owl < blue_jay, ["owl", "blue jay"])

# "The raven is to the left of the falcon"
problem.addConstraint(lambda raven, falcon: raven < falcon, ["raven", "falcon"])

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

# Find which bird is at position 1 (leftmost)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 1:
            print(letter)