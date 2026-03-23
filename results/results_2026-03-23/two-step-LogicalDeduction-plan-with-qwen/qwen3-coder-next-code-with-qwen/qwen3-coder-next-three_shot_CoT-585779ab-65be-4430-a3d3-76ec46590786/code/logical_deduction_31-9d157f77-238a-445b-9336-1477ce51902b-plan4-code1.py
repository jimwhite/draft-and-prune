from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (the five birds) and domain (positions 1 to 5)
birds = ["owl", "cardinal", "robin", "hummingbird", "crow"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add AllDifferent constraint to ensure each bird is in a unique position
problem.addConstraint(AllDifferentConstraint())

# Add positional constraints based on the problem description
# "The hummingbird is to the left of the owl" → hummingbird < owl
problem.addConstraint(lambda hummingbird, owl: hummingbird < owl, ("hummingbird", "owl"))

# "The hummingbird is to the right of the cardinal" → cardinal < hummingbird
problem.addConstraint(lambda cardinal, hummingbird: cardinal < hummingbird, ("cardinal", "hummingbird"))

# "The crow is to the left of the robin" → crow < robin
problem.addConstraint(lambda crow, robin: crow < robin, ("crow", "robin"))

# "The owl is to the left of the crow" → owl < crow
problem.addConstraint(lambda owl, crow: owl < crow, ("owl", "crow"))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names
choices = {
    "A": "owl",
    "B": "cardinal",
    "C": "robin",
    "D": "hummingbird",
    "E": "crow"
}

# Find which bird is at position 1 (leftmost) and print the corresponding choice letter
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 1:
            print(letter)