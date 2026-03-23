from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7, where 1 is highest finish)
golfers = ["Ana", "Eli", "Mya", "Amy", "Joe", "Mel", "Ada"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add constraint that all golfers have different positions
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "Ada finished above Mel" → Ada's position < Mel's position
problem.addConstraint(lambda ada, mel: ada < mel, ("Ada", "Mel"))

# "Ada finished third-to-last" → Ada's position = 5 (in a 7-person field: positions 5,6,7 are last three)
problem.addConstraint(lambda ada: ada == 5, ("Ada",))

# "Amy finished above Ana" → Amy's position < Ana's position
problem.addConstraint(lambda amy, ana: amy < ana, ("Amy", "Ana"))

# "Mya finished second-to-last" → Mya's position = 6
problem.addConstraint(lambda mya: mya == 6, ("Mya",))

# "Joe finished above Amy" → Joe's position < Amy's position
problem.addConstraint(lambda joe, amy: joe < amy, ("Joe", "Amy"))

# "Eli finished below Ana" → Eli's position > Ana's position
problem.addConstraint(lambda eli, ana: eli > ana, ("Eli", "Ana"))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    "A": "Ana",
    "B": "Eli",
    "C": "Mya",
    "D": "Amy",
    "E": "Joe",
    "F": "Mel",
    "G": "Ada"
}

# Find which golfer has position 3 (third place)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 3:
            print(letter)