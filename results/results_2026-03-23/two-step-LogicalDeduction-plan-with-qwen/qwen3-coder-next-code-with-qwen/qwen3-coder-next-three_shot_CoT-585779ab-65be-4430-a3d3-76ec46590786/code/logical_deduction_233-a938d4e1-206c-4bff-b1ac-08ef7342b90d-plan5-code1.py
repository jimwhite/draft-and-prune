from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7)
birds = ["robin", "hummingbird", "raven", "blue jay", "crow", "cardinal", "quail"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "The hummingbird is to the left of the crow"
problem.addConstraint(lambda hummingbird, crow: hummingbird < crow, ["hummingbird", "crow"])

# "The cardinal is to the right of the quail"
problem.addConstraint(lambda quail, cardinal: quail < cardinal, ["quail", "cardinal"])

# "The blue jay is the fourth from the left"
problem.addConstraint(lambda blue_jay: blue_jay == 4, ["blue jay"])

# "The robin is the second from the left"
problem.addConstraint(lambda robin: robin == 2, ["robin"])

# "The quail is to the right of the crow"
problem.addConstraint(lambda crow, quail: crow < quail, ["crow", "quail"])

# "The raven is to the left of the robin"
problem.addConstraint(lambda raven, robin: raven < robin, ["raven", "robin"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names
choices = {
    "A": "robin",
    "B": "hummingbird",
    "C": "raven",
    "D": "blue jay",
    "E": "crow",
    "F": "cardinal",
    "G": "quail"
}

# Find which bird is at position 3 (third from the left)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 3:
            print(letter)