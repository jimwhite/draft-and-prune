from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 5, left to right)
birds = ["hawk", "raven", "robin", "hummingbird", "crow"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "The robin is the leftmost" → robin = 1
problem.addConstraint(lambda robin: robin == 1, ["robin"])

# "The raven is the second from the left" → raven = 2
problem.addConstraint(lambda raven: raven == 2, ["raven"])

# "The hawk is the second from the right" → hawk = 4
problem.addConstraint(lambda hawk: hawk == 4, ["hawk"])

# "The crow is the third from the left" → crow = 3
problem.addConstraint(lambda crow: crow == 3, ["crow"])

# Solve the problem
solutions = problem.getSolutions()

# The question asks which bird is second from the right (position 4)
# According to constraints, hawk must be at position 4
# Map choices: A=hawk, B=raven, C=robin, D=hummingbird, E=crow
choices = {
    "A": "hawk",
    "B": "raven",
    "C": "robin",
    "D": "hummingbird",
    "E": "crow"
}

# Find which bird is at position 4 (second from right)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 4:
            print(letter)