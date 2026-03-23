from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7, left to right)
birds = ["falcon", "crow", "hawk", "hummingbird", "bluejay", "robin", "raven"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "The blue jay is to the right of the robin" → bluejay > robin
problem.addConstraint(lambda bluejay, robin: bluejay > robin, ("bluejay", "robin"))

# "The hawk is to the left of the hummingbird" → hawk < hummingbird
problem.addConstraint(lambda hawk, hummingbird: hawk < hummingbird, ("hawk", "hummingbird"))

# "The robin is the second from the right" → robin = 6
problem.addConstraint(lambda robin: robin == 6, ("robin",))

# "The falcon is the third from the left" → falcon = 3
problem.addConstraint(lambda falcon: falcon == 3, ("falcon",))

# "The crow is to the right of the hummingbird" → crow > hummingbird
problem.addConstraint(lambda crow, hummingbird: crow > hummingbird, ("crow", "hummingbird"))

# "The raven is the second from the left" → raven = 2
problem.addConstraint(lambda raven: raven == 2, ("raven",))

# Solve the problem
solutions = problem.getSolutions()

# The question asks which bird is third from the right (position 5)
# Map choice letters to bird names
choices = {
    "A": "falcon",
    "B": "crow",
    "C": "hawk",
    "D": "hummingbird",
    "E": "bluejay",
    "F": "robin",
    "G": "raven"
}

# Find which bird is at position 5 and print the corresponding letter
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 5:
            print(letter)