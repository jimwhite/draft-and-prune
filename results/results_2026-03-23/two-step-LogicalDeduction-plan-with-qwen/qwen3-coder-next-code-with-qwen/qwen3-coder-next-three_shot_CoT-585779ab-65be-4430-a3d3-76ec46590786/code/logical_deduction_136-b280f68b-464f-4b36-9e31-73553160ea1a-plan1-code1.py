from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7)
birds = ["blue_jay", "owl", "falcon", "hawk", "raven", "crow", "hummingbird"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "The falcon is the second from the left" → falcon == 2
problem.addConstraint(lambda falcon: falcon == 2, ["falcon"])

# "The crow is the rightmost" → crow == 7
problem.addConstraint(lambda crow: crow == 7, ["crow"])

# "The hummingbird is to the right of the blue jay" → blue_jay < hummingbird
problem.addConstraint(lambda blue_jay, hummingbird: blue_jay < hummingbird, ["blue_jay", "hummingbird"])

# "The hawk is to the right of the hummingbird" → hummingbird < hawk
problem.addConstraint(lambda hummingbird, hawk: hummingbird < hawk, ["hummingbird", "hawk"])

# "The blue jay is to the right of the owl" → owl < blue_jay
problem.addConstraint(lambda owl, blue_jay: owl < blue_jay, ["owl", "blue_jay"])

# "The raven is to the left of the falcon" → raven < 2 (so raven == 1)
problem.addConstraint(lambda raven: raven < 2, ["raven"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names
choices = {
    "A": "blue_jay",
    "B": "owl",
    "C": "falcon",
    "D": "hawk",
    "E": "raven",
    "F": "crow",
    "G": "hummingbird"
}

# Find the bird at position 1 (leftmost) and print corresponding choice letter
for solution in solutions:
    for bird_name, position in solution.items():
        if position == 1:
            # Find the choice letter corresponding to this bird
            for letter, name in choices.items():
                if name == bird_name:
                    print(letter)
            break