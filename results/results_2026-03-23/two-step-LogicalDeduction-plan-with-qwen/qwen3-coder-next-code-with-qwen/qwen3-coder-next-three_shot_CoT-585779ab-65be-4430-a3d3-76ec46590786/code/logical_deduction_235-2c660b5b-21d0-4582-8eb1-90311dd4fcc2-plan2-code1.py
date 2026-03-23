from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7, where 1=leftmost, 7=rightmost)
birds = ["hawk", "raven", "falcon", "crow", "hummingbird", "robin", "cardinal"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add all different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem statements:
# 1. "The hawk is the second from the right" → position = 6
problem.addConstraint(lambda hawk: hawk == 6, ["hawk"])

# 2. "The robin is to the left of the raven" → robin < raven
problem.addConstraint(lambda robin, raven: robin < raven, ["robin", "raven"])

# 3. "The raven is to the left of the crow" → raven < crow
problem.addConstraint(lambda raven, crow: raven < crow, ["raven", "crow"])

# 4. "The falcon is to the left of the cardinal" → falcon < cardinal
problem.addConstraint(lambda falcon, cardinal: falcon < cardinal, ["falcon", "cardinal"])

# 5. "The hummingbird is the second from the left" → position = 2
problem.addConstraint(lambda hummingbird: hummingbird == 2, ["hummingbird"])

# 6. "The falcon is the third from the right" → position = 5
problem.addConstraint(lambda falcon: falcon == 5, ["falcon"])

# Solve the problem
solutions = problem.getSolutions()

# The question asks which bird is second from the right (position 6)
# According to the problem statement, hawk is second from the right, so A should be correct
# Let's verify by checking which bird has position 6 in the solution

for solution in solutions:
    # Create mapping from choice letters to bird names
    choices = {
        "A": "hawk",
        "B": "raven",
        "C": "falcon",
        "D": "crow",
        "E": "hummingbird",
        "F": "robin",
        "G": "cardinal"
    }
    
    # Find which bird is at position 6
    for letter, bird_name in choices.items():
        if solution[bird_name] == 6:
            print(letter)
            break