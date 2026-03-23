from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (golfers) and domain (finishing positions 1-7, where 1 is first place)
golfers = ["Ana", "Eli", "Mya", "Amy", "Joe", "Mel", "Ada"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add constraints based on the problem description
# 1. All golfers must have unique positions
problem.addConstraint(AllDifferentConstraint())

# 2. "Ada finished above Mel" → ada_position < mel_position
problem.addConstraint(lambda ada, mel: ada < mel, ("Ada", "Mel"))

# 3. "Ada finished third-to-last" → position 5 (since 7 golfers: 1st,2nd,3rd,4th,5th=third-to-last,6th,7th)
problem.addConstraint(lambda ada: ada == 5, ("Ada",))

# 4. "Amy finished above Ana" → amy_position < ana_position
problem.addConstraint(lambda amy, ana: amy < ana, ("Amy", "Ana"))

# 5. "Mya finished second-to-last" → position 6
problem.addConstraint(lambda mya: mya == 6, ("Mya",))

# 6. "Joe finished above Amy" → joe_position < amy_position
problem.addConstraint(lambda joe, amy: joe < amy, ("Joe", "Amy"))

# 7. "Eli finished below Ana" → eli_position > ana_position
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

# Find who finished in position 3 (third place)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 3:
            print(letter)