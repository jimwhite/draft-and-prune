from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7)
birds = ["falcon", "owl", "quail", "raven", "hummingbird", "bluejay", "crow"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# 1. "The quail is to the left of the owl" → quail < owl
problem.addConstraint(lambda q, o: q < o, ["quail", "owl"])

# 2. "The owl is the second from the left" → owl == 2
problem.addConstraint(lambda o: o == 2, ["owl"])

# 3. "The crow is to the right of the falcon" → falcon < crow
problem.addConstraint(lambda f, c: f < c, ["falcon", "crow"])

# 4. "The blue jay is to the right of the hummingbird" → hummingbird < bluejay
problem.addConstraint(lambda h, b: h < b, ["hummingbird", "bluejay"])

# 5. "The hummingbird is to the right of the raven" → raven < hummingbird
problem.addConstraint(lambda r, h: r < h, ["raven", "hummingbird"])

# 6. "The blue jay is to the left of the falcon" → bluejay < falcon
problem.addConstraint(lambda b, f: b < f, ["bluejay", "falcon"])

# Solve the problem
solutions = problem.getSolutions()

# Map birds to choice letters for position 4 (fourth from left)
bird_to_choice = {
    "falcon": "A",
    "owl": "B",
    "quail": "C",
    "raven": "D",
    "hummingbird": "E",
    "bluejay": "F",
    "crow": "G"
}

# Find which bird is in position 4
for solution in solutions:
    for bird, pos in solution.items():
        if pos == 4:
            print(bird_to_choice[bird])