from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7)
birds = ["robin", "hummingbird", "raven", "bluejay", "crow", "cardinal", "quail"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# 1. "The hummingbird is to the left of the crow" → hummingbird < crow
problem.addConstraint(lambda h, c: h < c, ("hummingbird", "crow"))

# 2. "The cardinal is to the right of the quail" → quail < cardinal
problem.addConstraint(lambda q, ca: q < ca, ("quail", "cardinal"))

# 3. "The blue jay is the fourth from the left" → bluejay == 4
problem.addConstraint(lambda b: b == 4, ("bluejay",))

# 4. "The robin is the second from the left" → robin == 2
problem.addConstraint(lambda r: r == 2, ("robin",))

# 5. "The quail is to the right of the crow" → crow < quail
problem.addConstraint(lambda c, q: c < q, ("crow", "quail"))

# 6. "The raven is to the left of the robin" → raven < robin
problem.addConstraint(lambda ra, r: ra < r, ("raven", "robin"))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names
choices = {
    "A": "robin",
    "B": "hummingbird",
    "C": "raven",
    "D": "bluejay",
    "E": "crow",
    "F": "cardinal",
    "G": "quail"
}

# Find which bird is at position 7 (rightmost)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 7:
            print(letter)