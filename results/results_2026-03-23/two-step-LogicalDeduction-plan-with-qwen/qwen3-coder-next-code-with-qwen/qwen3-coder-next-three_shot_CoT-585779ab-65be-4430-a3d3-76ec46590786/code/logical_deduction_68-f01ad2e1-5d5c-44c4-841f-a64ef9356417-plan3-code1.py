from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 5, where 1 = first place, 5 = last)
golfers = ["mel", "dan", "amy", "joe", "eve"]
positions = range(1, 6)
problem.addVariables(golfers, positions)

# Add constraints
# All golfers have different finishing positions
problem.addConstraint(AllDifferentConstraint())

# "Amy finished below Dan" → amy's position > dan's position
problem.addConstraint(lambda amy, dan: amy > dan, ["amy", "dan"])

# "Mel finished first" → mel's position = 1
problem.addConstraint(lambda mel: mel == 1, ["mel"])

# "Joe finished above Dan" → joe's position < dan's position
problem.addConstraint(lambda joe, dan: joe < dan, ["joe", "dan"])

# "Eve finished last" → eve's position = 5
problem.addConstraint(lambda eve: eve == 5, ["eve"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to golfers
choices = {
    "A": "mel",
    "B": "dan",
    "C": "amy",
    "D": "joe",
    "E": "eve"
}

# Find which golfer finished last (position 5) and print the corresponding choice letter
for solution in solutions:
    for letter, golfer in choices.items():
        if solution[golfer] == 5:
            print(letter)