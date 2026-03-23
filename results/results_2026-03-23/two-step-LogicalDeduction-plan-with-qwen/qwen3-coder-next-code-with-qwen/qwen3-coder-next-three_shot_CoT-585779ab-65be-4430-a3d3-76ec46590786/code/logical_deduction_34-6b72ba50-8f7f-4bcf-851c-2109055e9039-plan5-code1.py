from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 5, where 1=leftmost, 5=rightmost)
birds = ["blue_jay", "robin", "cardinal", "hawk", "falcon"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints
# All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# "The blue jay is the rightmost" → position 5
problem.addConstraint(lambda blue_jay: blue_jay == 5, ["blue_jay"])

# "The robin is to the right of the falcon" → robin > falcon
problem.addConstraint(lambda robin, falcon: robin > falcon, ["robin", "falcon"])

# "The cardinal is to the left of the hawk" → cardinal < hawk
problem.addConstraint(lambda cardinal, hawk: cardinal < hawk, ["cardinal", "hawk"])

# "The falcon is to the right of the hawk" → falcon > hawk
problem.addConstraint(lambda falcon, hawk: falcon > hawk, ["falcon", "hawk"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names for "second from the right" (position 4)
choices = {
    "A": "blue_jay",
    "B": "robin",
    "C": "cardinal",
    "D": "hawk",
    "E": "falcon"
}

# Find which bird is at position 4 (second from the right)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 4:
            print(letter)