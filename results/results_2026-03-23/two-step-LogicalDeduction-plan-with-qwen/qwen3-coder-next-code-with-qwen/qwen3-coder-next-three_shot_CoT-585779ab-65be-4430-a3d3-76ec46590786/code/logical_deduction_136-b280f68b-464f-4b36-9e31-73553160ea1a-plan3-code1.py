from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7)
birds = ["blue jay", "owl", "falcon", "hawk", "raven", "crow", "hummingbird"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add all constraints
# All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# The falcon is the second from the left → position 2
problem.addConstraint(lambda falcon: falcon == 2, ["falcon"])

# The crow is the rightmost → position 7
problem.addConstraint(lambda crow: crow == 7, ["crow"])

# The hummingbird is to the right of the blue jay → blue_jay < hummingbird
problem.addConstraint(lambda blue_jay, hummingbird: blue_jay < hummingbird, ["blue jay", "hummingbird"])

# The hawk is to the right of the hummingbird → hummingbird < hawk
problem.addConstraint(lambda hummingbird, hawk: hummingbird < hawk, ["hummingbird", "hawk"])

# The blue jay is to the right of the owl → owl < blue_jay
problem.addConstraint(lambda owl, blue_jay: owl < blue_jay, ["owl", "blue jay"])

# The raven is to the left of the falcon → raven < falcon (and since falcon = 2, raven must be 1)
problem.addConstraint(lambda raven: raven < 2, ["raven"])

# Solve the problem
solutions = problem.getSolutions()

# Since we know raven < 2 and positions are integers starting at 1, raven must be 1
# Let's verify by checking the solution
solution = solutions[0]

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
for letter, bird_name in choices.items():
    if solution[bird_name] == 1:
        print(letter)