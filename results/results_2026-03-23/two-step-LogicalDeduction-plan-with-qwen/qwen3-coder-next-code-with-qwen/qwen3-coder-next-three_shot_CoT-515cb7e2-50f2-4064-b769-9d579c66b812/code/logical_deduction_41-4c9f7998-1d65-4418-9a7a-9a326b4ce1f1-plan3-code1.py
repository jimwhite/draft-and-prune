from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
birds = ["cardinal", "crow", "falcon", "robin", "blue jay"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "The robin is to the right of the cardinal" → cardinal < robin
problem.addConstraint(lambda cardinal, robin: cardinal < robin, ["cardinal", "robin"])

# "The cardinal is to the right of the blue jay" → blue jay < cardinal
problem.addConstraint(lambda blue_jay, cardinal: blue_jay < cardinal, ["blue jay", "cardinal"])

# "The blue jay is the second from the left" → blue_jay == 2
problem.addConstraint(lambda blue_jay: blue_jay == 2, ["blue jay"])

# "The crow is the rightmost" → crow == 5
problem.addConstraint(lambda crow: crow == 5, ["crow"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to birds
choices = {
    "A": "cardinal",
    "B": "crow",
    "C": "falcon",
    "D": "robin",
    "E": "blue jay"
}

# Find which bird is at position 1 (leftmost)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 1:
            print(letter)