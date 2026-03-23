from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7)
birds = ["cardinal", "bluejay", "robin", "falcon", "quail", "hummingbird", "raven"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add AllDifferent constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "The falcon is to the right of the quail" → falcon > quail
problem.addConstraint(lambda f, q: f > q, ["falcon", "quail"])

# "The robin is to the right of the hummingbird" → robin > hummingbird
problem.addConstraint(lambda r, h: r > h, ["robin", "hummingbird"])

# "The raven is to the left of the quail" → raven < quail
problem.addConstraint(lambda rv, q: rv < q, ["raven", "quail"])

# "The blue jay is the second from the left" → bluejay == 2
problem.addConstraint(lambda bj: bj == 2, ["bluejay"])

# "The robin is the third from the left" → robin == 3
problem.addConstraint(lambda r: r == 3, ["robin"])

# "The cardinal is the third from the right" → in a 7-position line, position = 7 - 2 = 5
problem.addConstraint(lambda c: c == 5, ["cardinal"])

# Solve the problem
solutions = problem.getSolutions()

# Map birds to choice letters for position 4 (fourth from left)
bird_to_choice = {
    "cardinal": "A",
    "bluejay": "B",
    "robin": "C",
    "falcon": "D",
    "quail": "E",
    "hummingbird": "F",
    "raven": "G"
}

# Find the bird at position 4 and print its choice letter
for solution in solutions:
    for bird, pos in solution.items():
        if pos == 4:
            print(bird_to_choice[bird])