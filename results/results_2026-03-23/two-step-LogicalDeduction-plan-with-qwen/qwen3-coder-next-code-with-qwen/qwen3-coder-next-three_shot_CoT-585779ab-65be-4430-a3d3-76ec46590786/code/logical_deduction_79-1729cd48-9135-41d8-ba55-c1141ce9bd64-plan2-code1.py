from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
birds = ["cardinal", "hawk", "hummingbird", "raven", "owl"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The raven is to the left of the hummingbird"
problem.addConstraint(lambda r, h: r < h, ("raven", "hummingbird"))

# "The hawk is to the left of the owl"
problem.addConstraint(lambda h, o: h < o, ("hawk", "owl"))

# "The cardinal is to the left of the hawk"
problem.addConstraint(lambda c, h: c < h, ("cardinal", "hawk"))

# "The raven is the second from the right" (position 4)
problem.addConstraint(lambda r: r == 4, ("raven",))

# Solve the problem
solutions = problem.getSolutions()

# Map choices to bird names
choices = {
    "A": "cardinal",
    "B": "hawk",
    "C": "hummingbird",
    "D": "raven",
    "E": "owl"
}

# Find which bird is at position 2 (second from the left)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 2:
            print(letter)