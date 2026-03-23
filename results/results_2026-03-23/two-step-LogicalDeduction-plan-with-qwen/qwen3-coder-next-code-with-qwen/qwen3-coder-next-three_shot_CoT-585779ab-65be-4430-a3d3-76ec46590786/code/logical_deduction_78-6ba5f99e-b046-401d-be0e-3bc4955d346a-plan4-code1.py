from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (birds) and domain (positions 1 to 5, where 1=leftmost, 5=rightmost)
birds = ["blue_jay", "raven", "crow", "falcon", "quail"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints based on the problem statements
# 1. All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The crow is to the left of the quail" → crow < quail
problem.addConstraint(lambda crow, quail: crow < quail, ("crow", "quail"))

# 3. "The falcon is the leftmost" → falcon == 1
problem.addConstraint(lambda falcon: falcon == 1, ["falcon"])

# 4. "The blue jay is to the right of the quail" → quail < blue_jay
problem.addConstraint(lambda quail, blue_jay: quail < blue_jay, ("quail", "blue_jay"))

# 5. "The raven is the second from the left" → raven == 2
problem.addConstraint(lambda raven: raven == 2, ["raven"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names
choices = {
    "A": "blue_jay",
    "B": "raven",
    "C": "crow",
    "D": "falcon",
    "E": "quail"
}

# Find which bird is at position 5 (rightmost)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 5:
            print(letter)