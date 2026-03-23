from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define the seven birds as variables
birds = ["cardinal", "blue jay", "robin", "falcon", "quail", "hummingbird", "raven"]

# Define the domain as positions 1 to 7 (1 = leftmost, 7 = rightmost)
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add AllDifferent constraint to ensure each bird is in a unique position
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "The falcon is to the right of the quail" → falcon > quail
problem.addConstraint(lambda falcon, quail: falcon > quail, ("falcon", "quail"))

# "The robin is to the right of the hummingbird" → robin > hummingbird
problem.addConstraint(lambda robin, hummingbird: robin > hummingbird, ("robin", "hummingbird"))

# "The raven is to the left of the quail" → raven < quail
problem.addConstraint(lambda raven, quail: raven < quail, ("raven", "quail"))

# "The blue jay is the second from the left" → blue jay == 2
problem.addConstraint(lambda blue_jay: blue_jay == 2, ["blue jay"])

# "The robin is the third from the left" → robin == 3
problem.addConstraint(lambda robin: robin == 3, ["robin"])

# "The cardinal is the third from the right" → in a 7-position line, this is position 5
problem.addConstraint(lambda cardinal: cardinal == 5, ["cardinal"])

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

# Find which bird is in position 6 (second from the right)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 6:
            print(letter)