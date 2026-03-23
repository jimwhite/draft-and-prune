from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7)
birds = ["hawk", "raven", "falcon", "crow", "hummingbird", "robin", "cardinal"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "The hawk is the second from the right" → position 6
problem.addConstraint(lambda hawk: hawk == 6, ["hawk"])

# "The robin is to the left of the raven" → robin < raven
problem.addConstraint(lambda robin, raven: robin < raven, ["robin", "raven"])

# "The raven is to the left of the crow" → raven < crow
problem.addConstraint(lambda raven, crow: raven < crow, ["raven", "crow"])

# "The falcon is to the left of the cardinal" → falcon < cardinal
problem.addConstraint(lambda falcon, cardinal: falcon < cardinal, ["falcon", "cardinal"])

# "The hummingbird is the second from the left" → position 2
problem.addConstraint(lambda hummingbird: hummingbird == 2, ["hummingbird"])

# "The falcon is the third from the right" → position 5 (since 7-3+1=5)
problem.addConstraint(lambda falcon: falcon == 5, ["falcon"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names
choices = {
    "A": "hawk",
    "B": "raven",
    "C": "falcon",
    "D": "crow",
    "E": "hummingbird",
    "F": "robin",
    "G": "cardinal"
}

# Find which bird is at position 6 (second from the right)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 6:
            print(letter)