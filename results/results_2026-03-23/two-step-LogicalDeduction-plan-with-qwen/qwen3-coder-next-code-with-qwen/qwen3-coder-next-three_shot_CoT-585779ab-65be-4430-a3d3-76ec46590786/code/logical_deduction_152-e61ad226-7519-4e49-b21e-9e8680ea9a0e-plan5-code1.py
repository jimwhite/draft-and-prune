from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7)
birds = ["hawk", "raven", "hummingbird", "falcon", "owl", "quail", "cardinal"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "The quail is to the left of the hummingbird" → quail < hummingbird
problem.addConstraint(lambda quail, hummingbird: quail < hummingbird, ["quail", "hummingbird"])

# "The raven is to the right of the hummingbird" → hummingbird < raven
problem.addConstraint(lambda hummingbird, raven: hummingbird < raven, ["hummingbird", "raven"])

# "The cardinal is the second from the left" → cardinal == 2
problem.addConstraint(lambda cardinal: cardinal == 2, ["cardinal"])

# "The owl is to the left of the cardinal" → owl < cardinal (i.e., owl < 2)
problem.addConstraint(lambda owl, cardinal: owl < cardinal, ["owl", "cardinal"])

# "The raven is the third from the right" → raven == 5 (since positions are 1-7, 7-3+1=5)
problem.addConstraint(lambda raven: raven == 5, ["raven"])

# "The falcon is the rightmost" → falcon == 7
problem.addConstraint(lambda falcon: falcon == 7, ["falcon"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names
choices = {
    "A": "hawk",
    "B": "raven",
    "C": "hummingbird",
    "D": "falcon",
    "E": "owl",
    "F": "quail",
    "G": "cardinal"
}

# Find which bird is at position 4 (fourth from the left)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 4:
            print(letter)