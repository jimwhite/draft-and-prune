from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 5, where 1 is leftmost)
birds = ["cardinal", "hawk", "hummingbird", "raven", "owl"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints
# All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# "The raven is to the left of the hummingbird"
problem.addConstraint(lambda r, h: r < h, ("raven", "hummingbird"))

# "The hawk is to the left of the owl"
problem.addConstraint(lambda hk, ow: hk < ow, ("hawk", "owl"))

# "The cardinal is to the left of the hawk"
problem.addConstraint(lambda ca, hk: ca < hk, ("cardinal", "hawk"))

# "The raven is the second from the right" (position 4 in a 5-position sequence)
problem.addConstraint(lambda r: r == 4, ("raven",))

# Solve the problem
solutions = problem.getSolutions()

# Map choices to birds
choices = {
    "A": "cardinal",
    "B": "hawk",
    "C": "hummingbird",
    "D": "raven",
    "E": "owl"
}

# Find the bird at position 1 (leftmost) and print corresponding choice letter
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 1:
            print(letter)