from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (the three birds) and domain (positions 1 to 3)
birds = ["hummingbird", "owl", "falcon"]
positions = range(1, 4)
problem.addVariables(birds, positions)

# Add constraints
# All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# "The falcon is to the right of the owl" => falcon > owl
problem.addConstraint(lambda falcon, owl: falcon > owl, ["falcon", "owl"])

# "The hummingbird is to the left of the owl" => hummingbird < owl
problem.addConstraint(lambda hummingbird, owl: hummingbird < owl, ["hummingbird", "owl"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names
choices = {
    "A": "hummingbird",
    "B": "owl",
    "C": "falcon"
}

# Find which bird is in position 2 (second from the left)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 2:
            print(letter)