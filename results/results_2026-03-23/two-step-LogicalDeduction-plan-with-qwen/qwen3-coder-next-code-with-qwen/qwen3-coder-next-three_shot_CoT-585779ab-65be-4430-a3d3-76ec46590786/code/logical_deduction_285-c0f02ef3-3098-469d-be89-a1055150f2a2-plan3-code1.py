from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables and domain for three birds
birds = ["falcon", "owl", "raven"]
positions = range(1, 4)  # 1=leftmost, 3=rightmost
problem.addVariables(birds, positions)

# Add constraints based on the problem statement
# 1. All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The raven is to the left of the owl" -> raven position < owl position
problem.addConstraint(lambda raven, owl: raven < owl, ["raven", "owl"])

# 3. "The falcon is the leftmost" -> falcon position == 1
problem.addConstraint(lambda falcon: falcon == 1, ["falcon"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to birds
choices = {
    "A": "falcon",
    "B": "owl",
    "C": "raven"
}

# Find which bird is rightmost (position 3) and print corresponding choice letter
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 3:
            print(letter)