from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (birds) and domain (positions 1 to 5, where 1 is leftmost)
birds = ["cardinal", "robin", "bluejay", "quail", "raven"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints based on the problem statements
# 1. All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The robin is to the right of the raven" → robin > raven
problem.addConstraint(lambda raven, robin: robin > raven, ["raven", "robin"])

# 3. "The cardinal is the leftmost" → cardinal == 1
problem.addConstraint(lambda cardinal: cardinal == 1, ["cardinal"])

# 4. "The raven is to the right of the blue jay" → raven > bluejay
problem.addConstraint(lambda bluejay, raven: raven > bluejay, ["bluejay", "raven"])

# 5. "The blue jay is the third from the left" → bluejay == 3
problem.addConstraint(lambda bluejay: bluejay == 3, ["bluejay"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names
choices = {
    "A": "cardinal",
    "B": "robin",
    "C": "bluejay",
    "D": "quail",
    "E": "raven"
}

# Find which bird is in position 2 (second from the left)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 2:
            print(letter)