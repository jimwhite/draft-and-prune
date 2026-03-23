from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
golfers = ["Amy", "Dan", "Mel"]
positions = range(1, 4)  # 1 = best (above), 3 = worst (below)
problem.addVariables(golfers, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "Mel finished above Amy" => mel's position < amy's position
problem.addConstraint(lambda mel, amy: mel < amy, ["Mel", "Amy"])

# "Dan finished below Amy" => amy's position < dan's position
problem.addConstraint(lambda amy, dan: amy < dan, ["Amy", "Dan"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to golfers
choices = {
    "A": "Amy",
    "B": "Dan",
    "C": "Mel"
}

# Find who finished last (position 3)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 3:
            print(letter)