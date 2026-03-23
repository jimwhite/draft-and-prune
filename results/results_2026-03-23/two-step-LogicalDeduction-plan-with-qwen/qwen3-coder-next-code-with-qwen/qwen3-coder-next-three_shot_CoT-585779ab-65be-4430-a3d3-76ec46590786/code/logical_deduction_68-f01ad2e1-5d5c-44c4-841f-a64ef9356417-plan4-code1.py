from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 5, where 1 = first place, 5 = last)
golfers = ["Mel", "Dan", "Amy", "Joe", "Eve"]
positions = range(1, 6)
problem.addVariables(golfers, positions)

# Add constraints
# All golfers have distinct positions
problem.addConstraint(AllDifferentConstraint())

# Mel finished first (position 1)
problem.addConstraint(lambda mel: mel == 1, ["Mel"])

# Eve finished last (position 5)
problem.addConstraint(lambda eve: eve == 5, ["Eve"])

# Amy finished below Dan (Amy's position > Dan's position)
problem.addConstraint(lambda amy, dan: amy > dan, ["Amy", "Dan"])

# Joe finished above Dan (Joe's position < Dan's position)
problem.addConstraint(lambda joe, dan: joe < dan, ["Joe", "Dan"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to golfers
choices = {
    "A": "Mel",
    "B": "Dan",
    "C": "Amy",
    "D": "Joe",
    "E": "Eve"
}

# Find which golfer is at position 5 (last place)
for solution in solutions:
    for letter, golfer in choices.items():
        if solution[golfer] == 5:
            print(letter)