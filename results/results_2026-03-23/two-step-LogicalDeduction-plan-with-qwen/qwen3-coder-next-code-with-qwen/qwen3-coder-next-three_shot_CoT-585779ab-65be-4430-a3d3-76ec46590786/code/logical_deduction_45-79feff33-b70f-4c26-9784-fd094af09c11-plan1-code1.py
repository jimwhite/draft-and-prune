from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (birds) and domain (positions 1 to 5, where 1=leftmost, 5=rightmost)
birds = ["cardinal", "robin", "bluejay", "quail", "raven"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem statements
# "The cardinal is the leftmost" → cardinal == 1
problem.addConstraint(lambda cardinal: cardinal == 1, ["cardinal"])

# "The blue jay is the third from the left" → bluejay == 3
problem.addConstraint(lambda bluejay: bluejay == 3, ["bluejay"])

# "The raven is to the right of the blue jay" → raven > bluejay
problem.addConstraint(lambda raven, bluejay: raven > bluejay, ["raven", "bluejay"])

# "The robin is to the right of the raven" → robin > raven
problem.addConstraint(lambda robin, raven: robin > raven, ["robin", "raven"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to birds for checking second-from-the-right (position 4)
choices = {
    "A": "cardinal",
    "B": "robin",
    "C": "bluejay",
    "D": "quail",
    "E": "raven"
}

# Find which bird is at position 4 (second from the right)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 4:
            print(letter)