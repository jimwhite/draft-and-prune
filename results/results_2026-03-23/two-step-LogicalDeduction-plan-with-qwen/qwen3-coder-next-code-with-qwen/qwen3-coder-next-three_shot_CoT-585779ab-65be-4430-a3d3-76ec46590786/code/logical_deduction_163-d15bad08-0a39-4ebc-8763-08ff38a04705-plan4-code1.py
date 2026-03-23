from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7)
birds = ["raven", "cardinal", "falcon", "owl", "bluejay", "quail", "robin"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add AllDifferent constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem statements
# "The owl is the second from the right" → position 6 (since 7 is rightmost)
problem.addConstraint(lambda owl: owl == 6, ["owl"])

# "The cardinal is the fourth from the left" → position 4
problem.addConstraint(lambda cardinal: cardinal == 4, ["cardinal"])

# "The falcon is to the left of the blue jay" → falcon < bluejay
problem.addConstraint(lambda falcon, bluejay: falcon < bluejay, ["falcon", "bluejay"])

# "The quail is to the left of the falcon" → quail < falcon
problem.addConstraint(lambda quail, falcon: quail < falcon, ["quail", "falcon"])

# "The raven is the second from the left" → position 2
problem.addConstraint(lambda raven: raven == 2, ["raven"])

# "The robin is to the left of the quail" → robin < quail
problem.addConstraint(lambda robin, quail: robin < quail, ["robin", "quail"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names
choices = {
    'A': 'raven',
    'B': 'cardinal',
    'C': 'falcon',
    'D': 'owl',
    'E': 'bluejay',
    'F': 'quail',
    'G': 'robin'
}

# Find the bird at position 1 (leftmost) and print corresponding choice letter
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 1:
            print(letter)