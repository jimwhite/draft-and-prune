from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (birds) and domain (positions 1 to 5, where 1 is leftmost)
birds = ["cardinal", "hawk", "hummingbird", "raven", "owl"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints based on the problem statements
# 1. All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The raven is to the left of the hummingbird" → raven < hummingbird
problem.addConstraint(lambda raven, hummingbird: raven < hummingbird, ("raven", "hummingbird"))

# 3. "The hawk is to the left of the owl" → hawk < owl
problem.addConstraint(lambda hawk, owl: hawk < owl, ("hawk", "owl"))

# 4. "The cardinal is to the left of the hawk" → cardinal < hawk
problem.addConstraint(lambda cardinal, hawk: cardinal < hawk, ("cardinal", "hawk"))

# 5. "The raven is the second from the right" → raven == 4
problem.addConstraint(lambda raven: raven == 4, ("raven",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names for the question about "second from the left" (position 2)
choices = {
    "A": "cardinal",
    "B": "hawk",
    "C": "hummingbird",
    "D": "raven",
    "E": "owl"
}

# Find which bird is at position 2 and print the corresponding choice letter
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 2:
            print(letter)