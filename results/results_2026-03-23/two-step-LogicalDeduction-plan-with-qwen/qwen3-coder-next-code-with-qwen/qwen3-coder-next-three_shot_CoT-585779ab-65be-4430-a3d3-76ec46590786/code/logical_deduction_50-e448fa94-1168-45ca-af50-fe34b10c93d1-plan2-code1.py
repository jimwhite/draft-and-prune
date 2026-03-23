from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
birds = ["crow", "falcon", "hawk", "robin", "quail"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The robin is the second from the left"
problem.addConstraint(lambda robin: robin == 2, ["robin"])

# "The hawk is the second from the right"
problem.addConstraint(lambda hawk: hawk == 4, ["hawk"])

# "The robin is to the right of the falcon"
problem.addConstraint(lambda falcon, robin: falcon < robin, ["falcon", "robin"])

# "The quail is to the left of the hawk"
problem.addConstraint(lambda quail, hawk: quail < hawk, ["quail", "hawk"])

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

# Find which bird is in position 3 (third from the left)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 3:
            print(letter)