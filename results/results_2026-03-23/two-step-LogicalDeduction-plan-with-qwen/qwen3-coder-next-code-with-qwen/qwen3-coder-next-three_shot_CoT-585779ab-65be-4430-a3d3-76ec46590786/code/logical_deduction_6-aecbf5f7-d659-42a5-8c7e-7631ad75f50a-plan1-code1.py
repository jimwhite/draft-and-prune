from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 5)
birds = ["crow", "robin", "quail", "blue jay", "falcon"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints based on the problem statement
# 1. All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The robin is to the left of the quail"
problem.addConstraint(lambda robin, quail: robin < quail, ["robin", "quail"])

# 3. "The falcon is the third from the left"
problem.addConstraint(lambda falcon: falcon == 3, ["falcon"])

# 4. "The crow is to the left of the falcon"
problem.addConstraint(lambda crow, falcon: crow < falcon, ["crow", "falcon"])

# 5. "The blue jay is the leftmost"
problem.addConstraint(lambda blue_jay: blue_jay == 1, ["blue jay"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to birds for checking who is third from the left (position 3)
choices = {
    "A": "crow",
    "B": "robin",
    "C": "quail",
    "D": "blue jay",
    "E": "falcon"
}

# Find which bird is at position 3 and print the corresponding choice letter
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 3:
            print(letter)