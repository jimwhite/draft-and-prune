from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
birds = ["crow", "falcon", "hawk", "robin", "quail"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The robin is to the right of the falcon" -> falcon < robin
problem.addConstraint(lambda falcon, robin: falcon < robin, ["falcon", "robin"])

# "The quail is to the left of the hawk" -> quail < hawk
problem.addConstraint(lambda quail, hawk: quail < hawk, ["quail", "hawk"])

# "The robin is the second from the left" -> robin == 2
problem.addConstraint(lambda robin: robin == 2, ["robin"])

# "The hawk is the second from the right" -> hawk == 4
problem.addConstraint(lambda hawk: hawk == 4, ["hawk"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to birds
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