from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (the seven birds)
birds = ["cardinal", "blue_jay", "robin", "falcon", "quail", "hummingbird", "raven"]

# Define domain: positions 1 to 7 (1 = leftmost, 7 = rightmost)
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add constraints based on the problem statement
# 1. All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The falcon is to the right of the quail" → falcon > quail
problem.addConstraint(lambda falcon, quail: falcon > quail, ("falcon", "quail"))

# 3. "The robin is to the right of the hummingbird" → robin > hummingbird
problem.addConstraint(lambda robin, hummingbird: robin > hummingbird, ("robin", "hummingbird"))

# 4. "The raven is to the left of the quail" → raven < quail
problem.addConstraint(lambda raven, quail: raven < quail, ("raven", "quail"))

# 5. "The blue jay is the second from the left" → blue_jay == 2
problem.addConstraint(lambda blue_jay: blue_jay == 2, ["blue_jay"])

# 6. "The robin is the third from the left" → robin == 3
problem.addConstraint(lambda robin: robin == 3, ["robin"])

# 7. "The cardinal is the third from the right" → position = 7 - 2 = 5
problem.addConstraint(lambda cardinal: cardinal == 5, ["cardinal"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names
choices = {
    'A': "cardinal",
    'B': "blue_jay",
    'C': "robin",
    'D': "falcon",
    'E': "quail",
    'F': "hummingbird",
    'G': "raven"
}

# Find which bird is at position 6 (second from the right)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 6:
            print(letter)