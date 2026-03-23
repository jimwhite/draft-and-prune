from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (the seven birds) and domain (positions 1 to 7)
birds = ["hawk", "hummingbird", "falcon", "cardinal", "owl", "robin", "blue jay"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add constraints
# All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# The hummingbird is to the left of the owl
problem.addConstraint(lambda h, o: h < o, ("hummingbird", "owl"))

# The robin is the rightmost
problem.addConstraint(lambda r: r == 7, ["robin"])

# The blue jay is to the left of the hawk
problem.addConstraint(lambda b, h: b < h, ("blue jay", "hawk"))

# The blue jay is the third from the left
problem.addConstraint(lambda b: b == 3, ["blue jay"])

# The falcon is the fourth from the left
problem.addConstraint(lambda f: f == 4, ["falcon"])

# The cardinal is the second from the right
problem.addConstraint(lambda c: c == 6, ["cardinal"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to birds
choices = {
    "A": "hawk",
    "B": "hummingbird",
    "C": "falcon",
    "D": "cardinal",
    "E": "owl",
    "F": "robin",
    "G": "blue jay"
}

# Find which bird is at position 7 (rightmost)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 7:
            print(letter)