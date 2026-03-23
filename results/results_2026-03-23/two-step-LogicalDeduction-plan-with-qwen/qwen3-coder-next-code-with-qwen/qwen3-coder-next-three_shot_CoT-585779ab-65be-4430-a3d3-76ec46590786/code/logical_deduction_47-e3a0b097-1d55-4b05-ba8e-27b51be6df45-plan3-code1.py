from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (the five birds)
birds = ["blue jay", "robin", "cardinal", "hawk", "falcon"]

# Define domain (positions 1 to 5, where 1 = leftmost, 5 = rightmost)
positions = range(1, 6)

# Add variables to the problem
problem.addVariables(birds, positions)

# Add constraint that all birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "The blue jay is the rightmost" → position 5
problem.addConstraint(lambda bj: bj == 5, ["blue jay"])

# "The robin is to the right of the falcon" → falcon < robin
problem.addConstraint(lambda falcon, robin: falcon < robin, ["falcon", "robin"])

# "The cardinal is to the left of the hawk" → cardinal < hawk
problem.addConstraint(lambda cardinal, hawk: cardinal < hawk, ["cardinal", "hawk"])

# "The falcon is to the right of the hawk" → hawk < falcon
problem.addConstraint(lambda hawk, falcon: hawk < falcon, ["hawk", "falcon"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to bird names
choices = {
    "A": "blue jay",
    "B": "robin",
    "C": "cardinal",
    "D": "hawk",
    "E": "falcon"
}

# Find which bird is at position 5 (rightmost) and print the corresponding choice letter
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 5:
            print(letter)