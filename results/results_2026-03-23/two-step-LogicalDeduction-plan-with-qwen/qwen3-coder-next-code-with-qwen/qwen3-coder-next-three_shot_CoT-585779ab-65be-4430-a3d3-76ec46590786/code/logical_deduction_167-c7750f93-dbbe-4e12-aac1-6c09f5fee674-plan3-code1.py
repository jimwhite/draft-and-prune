from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7)
birds = ["falcon", "crow", "hawk", "hummingbird", "bluejay", "robin", "raven"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "The blue jay is to the right of the robin"
problem.addConstraint(lambda robin, bluejay: bluejay > robin, ("robin", "bluejay"))

# "The hawk is to the left of the hummingbird"
problem.addConstraint(lambda hawk, hummingbird: hawk < hummingbird, ("hawk", "hummingbird"))

# "The robin is the second from the right" (position 6)
problem.addConstraint(lambda robin: robin == 6, ("robin",))

# "The falcon is the third from the left" (position 3)
problem.addConstraint(lambda falcon: falcon == 3, ("falcon",))

# "The crow is to the right of the hummingbird"
problem.addConstraint(lambda hummingbird, crow: crow > hummingbird, ("hummingbird", "crow"))

# "The raven is the second from the left" (position 2)
problem.addConstraint(lambda raven: raven == 2, ("raven",))

# Solve the problem
solutions = problem.getSolutions()

# Find which bird is at position 5 (third from the right)
solution = solutions[0]  # There should be exactly one solution

# Map choice letters to bird names
choices = {
    'A': "falcon",
    'B': "crow",
    'C': "hawk",
    'D': "hummingbird",
    'E': "bluejay",
    'F': "robin",
    'G': "raven"
}

# Find the bird at position 5 and print corresponding choice letter
for letter, bird_name in choices.items():
    if solution[bird_name] == 5:
        print(letter)