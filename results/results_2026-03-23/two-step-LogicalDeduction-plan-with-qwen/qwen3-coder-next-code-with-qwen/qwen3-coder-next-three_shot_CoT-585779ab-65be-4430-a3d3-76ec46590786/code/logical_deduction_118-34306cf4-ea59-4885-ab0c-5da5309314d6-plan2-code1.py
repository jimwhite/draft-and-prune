from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7, where 1 = best/first, 7 = last)
golfers = ["Eli", "Ada", "Amy", "Ana", "Eve", "Mel", "Dan"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add AllDifferent constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "Ada finished above Mel" → Ada's position < Mel's position
problem.addConstraint(lambda Ada, Mel: Ada < Mel, ["Ada", "Mel"])

# "Dan finished above Ada" → Dan's position < Ada's position
problem.addConstraint(lambda Dan, Ada: Dan < Ada, ["Dan", "Ada"])

# "Amy finished last" → Amy's position = 7
problem.addConstraint(lambda Amy: Amy == 7, ["Amy"])

# "Ana finished third-to-last" → In a 7-person field, position = 5
problem.addConstraint(lambda Ana: Ana == 5, ["Ana"])

# "Dan finished below Eli" → Dan's position > Eli's position (Eli < Dan)
problem.addConstraint(lambda Eli, Dan: Eli < Dan, ["Eli", "Dan"])

# "Eve finished third" → Eve's position = 3
problem.addConstraint(lambda Eve: Eve == 3, ["Eve"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfers
choices = {
    "A": "Eli",
    "B": "Ada",
    "C": "Amy",
    "D": "Ana",
    "E": "Eve",
    "F": "Mel",
    "G": "Dan"
}

# Find who finished third (position 3) and print the corresponding letter
for solution in solutions:
    for golfer, position in solution.items():
        if position == 3:
            # Find the choice letter corresponding to this golfer
            for letter, name in choices.items():
                if name == golfer:
                    print(letter)
            break