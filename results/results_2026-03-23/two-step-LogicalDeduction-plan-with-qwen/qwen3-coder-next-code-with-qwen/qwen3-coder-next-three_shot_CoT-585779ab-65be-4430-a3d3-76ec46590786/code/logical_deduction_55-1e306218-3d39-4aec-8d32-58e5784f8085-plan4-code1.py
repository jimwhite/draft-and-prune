from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 5, where 1=leftmost, 5=rightmost)
birds = ["crow", "falcon", "hawk", "robin", "quail"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints
# All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# "The robin is the second from the left" → robin == 2
problem.addConstraint(lambda robin: robin == 2, ["robin"])

# "The hawk is the second from the right" → hawk == 4
problem.addConstraint(lambda hawk: hawk == 4, ["hawk"])

# "The robin is to the right of the falcon" → falcon < robin (i.e., falcon < 2)
problem.addConstraint(lambda falcon, robin: falcon < robin, ["falcon", "robin"])

# "The quail is to the left of the hawk" → quail < hawk (i.e., quail < 4)
problem.addConstraint(lambda quail, hawk: quail < hawk, ["quail", "hawk"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to birds for the rightmost position (position 5)
choices = {
    "A": "crow",
    "B": "falcon",
    "C": "hawk",
    "D": "robin",
    "E": "quail"
}

# Find which bird is at position 5 (rightmost)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 5:
            print(letter)