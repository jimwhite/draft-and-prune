from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (the seven birds) and domain (positions 1 to 7)
birds = ["hawk", "hummingbird", "falcon", "cardinal", "owl", "robin", "blue jay"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add constraints based on the statements
# 1. All birds must be in unique positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The hummingbird is to the left of the owl"
problem.addConstraint(lambda hummingbird, owl: hummingbird < owl, ("hummingbird", "owl"))

# 3. "The robin is the rightmost"
problem.addConstraint(lambda robin: robin == 7, ("robin",))

# 4. "The blue jay is to the left of the hawk"
problem.addConstraint(lambda blue_jay, hawk: blue_jay < hawk, ("blue jay", "hawk"))

# 5. "The blue jay is the third from the left"
problem.addConstraint(lambda blue_jay: blue_jay == 3, ("blue jay",))

# 6. "The falcon is the fourth from the left"
problem.addConstraint(lambda falcon: falcon == 4, ("falcon",))

# 7. "The cardinal is the second from the right"
problem.addConstraint(lambda cardinal: cardinal == 6, ("cardinal",))

# Solve the problem
solutions = problem.getSolutions()

# Map answer choices to bird names
choices = {
    "A": "hawk",
    "B": "hummingbird",
    "C": "falcon",
    "D": "cardinal",
    "E": "owl",
    "F": "robin",
    "G": "blue jay"
}

# Find which bird is at position 3 (third from the left)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 3:
            print(letter)