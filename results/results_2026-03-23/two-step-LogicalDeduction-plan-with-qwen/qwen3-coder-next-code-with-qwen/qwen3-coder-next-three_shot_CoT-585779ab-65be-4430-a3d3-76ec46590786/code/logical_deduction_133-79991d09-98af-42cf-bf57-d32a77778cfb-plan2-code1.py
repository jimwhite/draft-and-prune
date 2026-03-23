from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7)
birds = ["cardinal", "blue jay", "robin", "falcon", "quail", "hummingbird", "raven"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add AllDifferentConstraint to ensure each bird is in a unique position
problem.addConstraint(AllDifferentConstraint())

# Add positional constraints based on the problem description
# "The blue jay is the second from the left" → position 2
problem.addConstraint(lambda bj: bj == 2, ["blue jay"])

# "The robin is the third from the left" → position 3
problem.addConstraint(lambda robin: robin == 3, ["robin"])

# "The cardinal is the third from the right" → position 5 (since 7-3+1=5)
problem.addConstraint(lambda cardinal: cardinal == 5, ["cardinal"])

# "The raven is to the left of the quail" → raven < quail
problem.addConstraint(lambda raven, quail: raven < quail, ["raven", "quail"])

# "The falcon is to the right of the quail" → quail < falcon
problem.addConstraint(lambda quail, falcon: quail < falcon, ["quail", "falcon"])

# "The robin is to the right of the hummingbird" → hummingbird < robin (robin == 3, so hummingbird < 3)
problem.addConstraint(lambda hummingbird, robin: hummingbird < robin, ["hummingbird", "robin"])

# Solve the problem
solutions = problem.getSolutions()

# Get the unique solution (problem has exactly one solution)
solution = solutions[0]

# Determine which bird is at position 4 (fourth from the left)
bird_at_position_4 = None
for bird, pos in solution.items():
    if pos == 4:
        bird_at_position_4 = bird
        break

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

# Find the choice letter corresponding to the bird at position 4
for letter, bird_name in choices.items():
    if bird_name == bird_at_position_4:
        print(letter)
        break