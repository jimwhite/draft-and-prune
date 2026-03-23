from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7)
birds = ["robin", "hummingbird", "raven", "bluejay", "crow", "cardinal", "quail"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add all different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem description:
# 1. The hummingbird is to the left of the crow
problem.addConstraint(lambda hummingbird, crow: hummingbird < crow, ["hummingbird", "crow"])

# 2. The cardinal is to the right of the quail
problem.addConstraint(lambda quail, cardinal: quail < cardinal, ["quail", "cardinal"])

# 3. The blue jay is the fourth from the left
problem.addConstraint(lambda bluejay: bluejay == 4, ["bluejay"])

# 4. The robin is the second from the left
problem.addConstraint(lambda robin: robin == 2, ["robin"])

# 5. The quail is to the right of the crow
problem.addConstraint(lambda crow, quail: crow < quail, ["crow", "quail"])

# 6. The raven is to the left of the robin
problem.addConstraint(lambda raven, robin: raven < robin, ["raven", "robin"])

# Solve the problem
solutions = problem.getSolutions()

# Map birds to choice letters
bird_to_choice = {
    "robin": "A",
    "hummingbird": "B",
    "raven": "C",
    "bluejay": "D",
    "crow": "E",
    "cardinal": "F",
    "quail": "G"
}

# Find the bird at position 7 (rightmost) and print its choice letter
for solution in solutions:
    for bird, position in solution.items():
        if position == 7:
            print(bird_to_choice[bird])