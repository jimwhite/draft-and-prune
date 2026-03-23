from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7)
golfers = ["Joe", "Eli", "Ada", "Mel", "Eve", "Rob", "Ana"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add AllDifferentConstraint to ensure unique placements
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "Joe finished first" → Joe's position = 1
problem.addConstraint(lambda Joe: Joe == 1, ["Joe"])

# "Mel finished second-to-last" → Mel's position = 6
problem.addConstraint(lambda Mel: Mel == 6, ["Mel"])

# "Rob finished above Eve" → Rob's position < Eve's position
problem.addConstraint(lambda Rob, Eve: Rob < Eve, ["Rob", "Eve"])

# "Mel finished above Eli" → Mel's position < Eli's position
problem.addConstraint(lambda Mel, Eli: Mel < Eli, ["Mel", "Eli"])

# "Rob finished below Ada" → Rob's position > Ada's position
problem.addConstraint(lambda Rob, Ada: Rob > Ada, ["Rob", "Ada"])

# "Eve finished fourth" → Eve's position = 4
problem.addConstraint(lambda Eve: Eve == 4, ["Eve"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfers
choices = {
    "A": "Joe",
    "B": "Eli",
    "C": "Ada",
    "D": "Mel",
    "E": "Eve",
    "F": "Rob",
    "G": "Ana"
}

# Find the golfer in position 7 (last place)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 7:
            print(letter)