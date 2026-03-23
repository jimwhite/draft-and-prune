from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 5, where 1=leftmost, 5=rightmost)
birds = ["falcon", "raven", "cardinal", "hawk", "crow"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints
# All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# "The cardinal is the second from the right" → position 4
problem.addConstraint(lambda cardinal: cardinal == 4, ["cardinal"])

# "The raven is the second from the left" → position 2
problem.addConstraint(lambda raven: raven == 2, ["raven"])

# "The crow is the rightmost" → position 5
problem.addConstraint(lambda crow: crow == 5, ["crow"])

# "The hawk is to the right of the falcon" → falcon < hawk
problem.addConstraint(lambda falcon, hawk: falcon < hawk, ["falcon", "hawk"])

# Solve the problem
solutions = problem.getSolutions()

# The question asks which bird is second from the left (position 2)
# Map choices to birds
choices = {
    "A": "falcon",
    "B": "raven",
    "C": "cardinal",
    "D": "hawk",
    "E": "crow"
}

# Find which bird is at position 2 in the solution
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 2:
            print(letter)