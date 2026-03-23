from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (the five birds) and domain (positions 1 to 5)
birds = ["owl", "crow", "raven", "robin", "cardinal"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints based on the problem statements
# 1. All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The raven is the second from the left" → raven == 2
problem.addConstraint(lambda raven: raven == 2, ["raven"])

# 3. "The raven is to the right of the owl" → owl < raven (owl < 2)
problem.addConstraint(lambda owl, raven: owl < raven, ["owl", "raven"])

# 4. "The robin is the second from the right" → robin == 4
problem.addConstraint(lambda robin: robin == 4, ["robin"])

# 5. "The robin is to the left of the crow" → robin < crow (4 < crow, so crow == 5)
problem.addConstraint(lambda robin, crow: robin < crow, ["robin", "crow"])

# Solve the problem
solutions = problem.getSolutions()

# The question asks which bird is second from the left (position 2)
choices = {
    "A": "owl",
    "B": "crow",
    "C": "raven",
    "D": "robin",
    "E": "cardinal"
}

# Find which bird is at position 2 and print the corresponding letter
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 2:
            print(letter)