from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (birds) and domain (positions 1 to 5, where 1=leftmost, 5=rightmost)
birds = ["blue_jay", "robin", "cardinal", "hawk", "falcon"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraint that all birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem statements:
# 1. "The blue jay is the rightmost" → position = 5
problem.addConstraint(lambda blue_jay: blue_jay == 5, ["blue_jay"])

# 2. "The robin is to the right of the falcon" → falcon < robin
problem.addConstraint(lambda falcon, robin: falcon < robin, ["falcon", "robin"])

# 3. "The cardinal is to the left of the hawk" → cardinal < hawk
problem.addConstraint(lambda cardinal, hawk: cardinal < hawk, ["cardinal", "hawk"])

# 4. "The falcon is to the right of the hawk" → hawk < falcon
problem.addConstraint(lambda hawk, falcon: hawk < falcon, ["hawk", "falcon"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names
choices = {
    "A": "blue_jay",
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