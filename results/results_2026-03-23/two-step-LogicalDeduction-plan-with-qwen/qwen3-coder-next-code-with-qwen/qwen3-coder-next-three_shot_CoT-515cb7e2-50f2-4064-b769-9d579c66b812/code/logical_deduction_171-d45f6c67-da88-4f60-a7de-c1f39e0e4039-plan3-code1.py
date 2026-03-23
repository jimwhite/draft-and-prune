from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7, where 1 = first place)
golfers = ["Ana", "Eli", "Mya", "Amy", "Joe", "Mel", "Ada"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "Ada finished above Mel" → ada_pos < mel_pos
problem.addConstraint(lambda ada, mel: ada < mel, ("Ada", "Mel"))

# "Ada finished third-to-last" → with 7 golfers, third-to-last = position 5
problem.addConstraint(lambda ada: ada == 5, ("Ada",))

# "Amy finished above Ana" → amy_pos < ana_pos
problem.addConstraint(lambda amy, ana: amy < ana, ("Amy", "Ana"))

# "Mya finished second-to-last" → mya_pos = 6
problem.addConstraint(lambda mya: mya == 6, ("Mya",))

# "Joe finished above Amy" → joe_pos < amy_pos
problem.addConstraint(lambda joe, amy: joe < amy, ("Joe", "Amy"))

# "Eli finished below Ana" → eli_pos > ana_pos
problem.addConstraint(lambda eli, ana: eli > ana, ("Eli", "Ana"))

# Solve the problem
solutions = problem.getSolutions()

# Map choices to golfers
choices = {
    "A": "Ana",
    "B": "Eli",
    "C": "Mya",
    "D": "Amy",
    "E": "Joe",
    "F": "Mel",
    "G": "Ada"
}

# Find which golfer finished third (position 3)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 3:
            print(letter)