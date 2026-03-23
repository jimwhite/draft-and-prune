from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (the seven birds)
birds = ["hawk", "hummingbird", "falcon", "cardinal", "owl", "robin", "blue jay"]

# Define domain: positions 1 to 7 (1 = leftmost, 7 = rightmost)
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "The hummingbird is to the left of the owl"
problem.addConstraint(lambda hummingbird, owl: hummingbird < owl, ["hummingbird", "owl"])

# "The robin is the rightmost"
problem.addConstraint(lambda robin: robin == 7, ["robin"])

# "The blue jay is to the left of the hawk"
problem.addConstraint(lambda blue_jay, hawk: blue_jay < hawk, ["blue jay", "hawk"])

# "The blue jay is the third from the left"
problem.addConstraint(lambda blue_jay: blue_jay == 3, ["blue jay"])

# "The falcon is the fourth from the left"
problem.addConstraint(lambda falcon: falcon == 4, ["falcon"])

# "The cardinal is the second from the right"
problem.addConstraint(lambda cardinal: cardinal == 6, ["cardinal"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names
choices = {
    "A": "hawk",
    "B": "hummingbird",
    "C": "falcon",
    "D": "cardinal",
    "E": "owl",
    "F": "robin",
    "G": "blue jay"
}

# Find the bird at position 7 (rightmost) and print corresponding choice letter
for solution in solutions:
    for bird_name, position in solution.items():
        if position == 7:
            # Find the choice letter corresponding to this bird
            for letter, choice_bird in choices.items():
                if choice_bird == bird_name:
                    print(letter)
            break