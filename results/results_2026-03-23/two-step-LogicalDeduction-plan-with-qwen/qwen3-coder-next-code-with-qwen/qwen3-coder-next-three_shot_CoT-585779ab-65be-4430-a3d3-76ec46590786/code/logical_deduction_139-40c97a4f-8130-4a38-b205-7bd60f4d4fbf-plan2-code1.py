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
# "The hummingbird is to the left of the crow" → hummingbird < crow
problem.addConstraint(lambda hummingbird, crow: hummingbird < crow, ("hummingbird", "crow"))

# "The cardinal is to the right of the quail" → cardinal > quail
problem.addConstraint(lambda quail, cardinal: cardinal > quail, ("quail", "cardinal"))

# "The blue jay is the fourth from the left" → bluejay == 4
problem.addConstraint(lambda bluejay: bluejay == 4, ("bluejay",))

# "The robin is the second from the left" → robin == 2
problem.addConstraint(lambda robin: robin == 2, ("robin",))

# "The quail is to the right of the crow" → quail > crow
problem.addConstraint(lambda crow, quail: quail > crow, ("crow", "quail"))

# "The raven is to the left of the robin" → raven < robin (and since robin == 2, raven must be 1)
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

# Find the bird at position 7 (rightmost)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 7:
            print(letter)