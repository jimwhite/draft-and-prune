from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7)
birds = ["hummingbird", "cardinal", "blue_jay", "owl", "raven", "quail", "robin"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add AllDifferent constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "The hummingbird is to the left of the quail"
problem.addConstraint(lambda h, q: h < q, ["hummingbird", "quail"])

# "The robin is to the left of the cardinal"
problem.addConstraint(lambda r, c: r < c, ["robin", "cardinal"])

# "The blue jay is the leftmost"
problem.addConstraint(lambda bj: bj == 1, ["blue_jay"])

# "The cardinal is the fourth from the left"
problem.addConstraint(lambda c: c == 4, ["cardinal"])

# "The raven is the third from the right" (positions 5,6,7 are rightmost three, so raven is at position 5)
problem.addConstraint(lambda rv: rv == 5, ["raven"])

# "The owl is the third from the left"
problem.addConstraint(lambda o: o == 3, ["owl"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names
choices = {
    "A": "hummingbird",
    "B": "cardinal",
    "C": "blue_jay",
    "D": "owl",
    "E": "raven",
    "F": "quail",
    "G": "robin"
}

# Find which bird is at position 1 (leftmost)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 1:
            print(letter)