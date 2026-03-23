from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7)
birds = ["quail", "raven", "hummingbird", "robin", "falcon", "owl", "blue jay"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add AllDifferent constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "The blue jay is to the left of the falcon"
problem.addConstraint(lambda b, f: b < f, ["blue jay", "falcon"])

# "The blue jay is the second from the right" -> position 6
problem.addConstraint(lambda b: b == 6, ["blue jay"])

# "The raven is to the left of the robin"
problem.addConstraint(lambda r, ro: r < ro, ["raven", "robin"])

# "The owl is the third from the right" -> position 5 (7-2=5)
problem.addConstraint(lambda o: o == 5, ["owl"])

# "The hummingbird is to the left of the quail"
problem.addConstraint(lambda h, q: h < q, ["hummingbird", "quail"])

# "The raven is the third from the left" -> position 3
problem.addConstraint(lambda r: r == 3, ["raven"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to birds
choices = {
    "A": "quail",
    "B": "raven",
    "C": "hummingbird",
    "D": "robin",
    "E": "falcon",
    "F": "owl",
    "G": "blue jay"
}

# Find which bird is at position 4 (fourth from the left)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 4:
            print(letter)