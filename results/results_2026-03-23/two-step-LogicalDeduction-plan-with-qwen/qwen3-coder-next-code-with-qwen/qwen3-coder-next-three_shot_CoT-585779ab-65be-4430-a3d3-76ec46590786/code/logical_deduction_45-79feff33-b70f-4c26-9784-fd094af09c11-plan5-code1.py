from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (the five birds)
birds = ["cardinal", "robin", "blue jay", "quail", "raven"]

# Define domain (positions 1 to 5, where 1 = leftmost, 5 = rightmost)
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints based on the problem statement
# 1. All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The robin is to the right of the raven" => robin > raven
problem.addConstraint(lambda robin, raven: robin > raven, ["robin", "raven"])

# 3. "The cardinal is the leftmost" => cardinal == 1
problem.addConstraint(lambda cardinal: cardinal == 1, ["cardinal"])

# 4. "The raven is to the right of the blue jay" => raven > blue jay
problem.addConstraint(lambda raven, blue_jay: raven > blue_jay, ["raven", "blue jay"])

# 5. "The blue jay is the third from the left" => blue jay == 3
problem.addConstraint(lambda blue_jay: blue_jay == 3, ["blue jay"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to birds (the bird that is second from the right, i.e., position 4)
choices = {
    "A": "cardinal",
    "B": "robin",
    "C": "blue jay",
    "D": "quail",
    "E": "raven"
}

# Find which bird is at position 4 (second from the right)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 4:
            print(letter)