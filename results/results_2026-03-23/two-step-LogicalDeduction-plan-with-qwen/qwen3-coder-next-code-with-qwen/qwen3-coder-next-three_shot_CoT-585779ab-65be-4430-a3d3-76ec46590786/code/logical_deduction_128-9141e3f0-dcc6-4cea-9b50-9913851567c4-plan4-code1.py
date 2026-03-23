from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7)
birds = ["robin", "hummingbird", "raven", "bluejay", "crow", "cardinal", "quail"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add all different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# 1. "The hummingbird is to the left of the crow" → hummingbird < crow
problem.addConstraint(lambda hummingbird, crow: hummingbird < crow, ("hummingbird", "crow"))

# 2. "The cardinal is to the right of the quail" → quail < cardinal
problem.addConstraint(lambda quail, cardinal: quail < cardinal, ("quail", "cardinal"))

# 3. "The blue jay is the fourth from the left" → bluejay == 4
problem.addConstraint(lambda bluejay: bluejay == 4, ("bluejay",))

# 4. "The robin is the second from the left" → robin == 2
problem.addConstraint(lambda robin: robin == 2, ("robin",))

# 5. "The quail is to the right of the crow" → crow < quail
problem.addConstraint(lambda crow, quail: crow < quail, ("crow", "quail"))

# 6. "The raven is to the left of the robin" → raven < robin (and since robin == 2, raven must be 1)
problem.addConstraint(lambda raven, robin: raven < robin, ("raven", "robin"))

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

# Find which bird is at position 2 (second from the left)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 2:
            print(letter)