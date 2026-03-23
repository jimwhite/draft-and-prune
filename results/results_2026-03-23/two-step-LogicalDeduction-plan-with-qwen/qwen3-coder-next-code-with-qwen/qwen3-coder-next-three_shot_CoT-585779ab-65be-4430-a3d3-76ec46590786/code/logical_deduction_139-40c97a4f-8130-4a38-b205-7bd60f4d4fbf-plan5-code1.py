from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (the seven birds)
birds = ["robin", "hummingbird", "raven", "bluejay", "crow", "cardinal", "quail"]

# Define domain: positions 1 to 7 (1 = leftmost, 7 = rightmost)
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add constraints based on the statements
# 1. All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The hummingbird is to the left of the crow" → hummingbird < crow
problem.addConstraint(lambda hummingbird, crow: hummingbird < crow, ("hummingbird", "crow"))

# 3. "The cardinal is to the right of the quail" → quail < cardinal
problem.addConstraint(lambda quail, cardinal: quail < cardinal, ("quail", "cardinal"))

# 4. "The blue jay is the fourth from the left" → bluejay == 4
problem.addConstraint(lambda bluejay: bluejay == 4, ("bluejay",))

# 5. "The robin is the second from the left" → robin == 2
problem.addConstraint(lambda robin: robin == 2, ("robin",))

# 6. "The quail is to the right of the crow" → crow < quail
problem.addConstraint(lambda crow, quail: crow < quail, ("crow", "quail"))

# 7. "The raven is to the left of the robin" → raven < robin
problem.addConstraint(lambda raven, robin: raven < robin, ("raven", "robin"))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names
choices = {
    "A": "robin",
    "B": "hummingbird",
    "C": "raven",
    "D": "bluejay",
    "E": "crow",
    "F": "cardinal",
    "G": "quail"
}

# Find which bird is at position 7 (rightmost)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 7:
            print(letter)