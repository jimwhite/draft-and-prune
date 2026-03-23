from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 7)
birds = ["falcon", "crow", "hawk", "hummingbird", "bluejay", "robin", "raven"]
positions = range(1, 8)
problem.addVariables(birds, positions)

# Add all different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# 1. "The blue jay is to the right of the robin" → bluejay > robin
problem.addConstraint(lambda b, r: b > r, ("bluejay", "robin"))

# 2. "The hawk is to the left of the hummingbird" → hawk < hummingbird
problem.addConstraint(lambda h, m: h < m, ("hawk", "hummingbird"))

# 3. "The robin is the second from the right" → robin = 6
problem.addConstraint(lambda r: r == 6, ("robin",))

# 4. "The falcon is the third from the left" → falcon = 3
problem.addConstraint(lambda f: f == 3, ("falcon",))

# 5. "The crow is to the right of the hummingbird" → crow > hummingbird
problem.addConstraint(lambda c, m: c > m, ("crow", "hummingbird"))

# 6. "The raven is the second from the left" → raven = 2
problem.addConstraint(lambda rv: rv == 2, ("raven",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names
choices = {
    'A': 'falcon',
    'B': 'crow',
    'C': 'hawk',
    'D': 'hummingbird',
    'E': 'bluejay',
    'F': 'robin',
    'G': 'raven'
}

# Find which bird is at position 5 (third from the right)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 5:
            print(letter)