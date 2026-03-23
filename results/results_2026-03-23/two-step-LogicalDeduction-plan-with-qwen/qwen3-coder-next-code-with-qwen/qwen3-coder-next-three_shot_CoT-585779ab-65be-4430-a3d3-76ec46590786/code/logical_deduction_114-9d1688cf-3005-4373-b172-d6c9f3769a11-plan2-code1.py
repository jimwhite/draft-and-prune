from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7)
birds = ["blue jay", "owl", "falcon", "hawk", "raven", "crow", "hummingbird"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add AllDifferentConstraint to ensure unique positions
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

# The second-from-right position is 6 (since rightmost is 7)
second_from_right_pos = 6

# Map choice letters to birds
choices = {
    "A": "blue jay",
    "B": "owl",
    "C": "falcon",
    "D": "hawk",
    "E": "raven",
    "F": "crow",
    "G": "hummingbird"
}

# Find which bird is at position 6 and print the corresponding choice letter
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == second_from_right_pos:
            print(letter)