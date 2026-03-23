from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7)
birds = ["cardinal", "blue jay", "robin", "falcon", "quail", "hummingbird", "raven"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "The falcon is to the right of the quail" → quail < falcon
problem.addConstraint(lambda q, f: q < f, ["quail", "falcon"])

# "The robin is to the right of the hummingbird" → hummingbird < robin
problem.addConstraint(lambda h, r: h < r, ["hummingbird", "robin"])

# "The raven is to the left of the quail" → raven < quail
problem.addConstraint(lambda r, q: r < q, ["raven", "quail"])

# "The blue jay is the second from the left" → position 2
problem.addConstraint(lambda bj: bj == 2, ["blue jay"])

# "The robin is the third from the left" → position 3
problem.addConstraint(lambda r: r == 3, ["robin"])

# "The cardinal is the third from the right" → position 5 (since 7-2=5)
problem.addConstraint(lambda c: c == 5, ["cardinal"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names
choices = {
    "A": "cardinal",
    "B": "blue jay",
    "C": "robin",
    "D": "falcon",
    "E": "quail",
    "F": "hummingbird",
    "G": "raven"
}

# Find which bird is at position 5 (third from the right)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 5:
            print(letter)