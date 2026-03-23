from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (the seven birds) and domain (positions 1 to 7)
birds = ["hawk", "raven", "falcon", "crow", "hummingbird", "robin", "cardinal"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add constraints based on the problem statements
# 1. All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The hawk is the second from the right" → position 6
problem.addConstraint(lambda hawk: hawk == 6, ["hawk"])

# 3. "The robin is to the left of the raven" → robin < raven
problem.addConstraint(lambda robin, raven: robin < raven, ["robin", "raven"])

# 4. "The raven is to the left of the crow" → raven < crow
problem.addConstraint(lambda raven, crow: raven < crow, ["raven", "crow"])

# 5. "The falcon is to the left of the cardinal" → falcon < cardinal
problem.addConstraint(lambda falcon, cardinal: falcon < cardinal, ["falcon", "cardinal"])

# 6. "The hummingbird is the second from the left" → position 2
problem.addConstraint(lambda hummingbird: hummingbird == 2, ["hummingbird"])

# 7. "The falcon is the third from the right" → position 5 (since 7-2=5)
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
            break
    break