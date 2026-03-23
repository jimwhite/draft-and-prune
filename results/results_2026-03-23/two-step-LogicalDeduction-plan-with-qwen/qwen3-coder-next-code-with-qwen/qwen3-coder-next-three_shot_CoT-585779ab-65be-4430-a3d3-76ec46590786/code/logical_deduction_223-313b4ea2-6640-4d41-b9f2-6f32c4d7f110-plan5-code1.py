from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7)
birds = ["hummingbird", "cardinal", "blue jay", "owl", "raven", "quail", "robin"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add AllDifferent constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "The hummingbird is to the left of the quail"
problem.addConstraint(lambda hummingbird, quail: hummingbird < quail, ["hummingbird", "quail"])

# "The robin is to the left of the cardinal"
problem.addConstraint(lambda robin, cardinal: robin < cardinal, ["robin", "cardinal"])

# "The blue jay is the leftmost" (position 1)
problem.addConstraint(lambda blue_jay: blue_jay == 1, ["blue jay"])

# "The cardinal is the fourth from the left" (position 4)
problem.addConstraint(lambda cardinal: cardinal == 4, ["cardinal"])

# "The raven is the third from the right" (position 5 in a 7-position line)
problem.addConstraint(lambda raven: raven == 5, ["raven"])

# "The owl is the third from the left" (position 3)
problem.addConstraint(lambda owl: owl == 3, ["owl"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names
choices = {
    "A": "hummingbird",
    "B": "cardinal",
    "C": "blue jay",
    "D": "owl",
    "E": "raven",
    "F": "quail",
    "G": "robin"
}

# Find the bird at position 1 (leftmost) and print corresponding choice letter
for solution in solutions:
    for bird_name, position in solution.items():
        if position == 1:
            # Find the choice letter corresponding to this bird
            for letter, name in choices.items():
                if name == bird_name:
                    print(letter)
            break