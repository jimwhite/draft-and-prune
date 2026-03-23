from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
birds = ["hummingbird", "owl", "falcon"]
positions = range(1, 4)
problem.addVariables(birds, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The falcon is to the right of the owl" => falcon > owl
problem.addConstraint(lambda falcon, owl: falcon > owl, ("falcon", "owl"))

# "The hummingbird is to the left of the owl" => hummingbird < owl
problem.addConstraint(lambda hummingbird, owl: hummingbird < owl, ("hummingbird", "owl"))

# Solve the problem
solutions = problem.getSolutions()

# Map choices to birds
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