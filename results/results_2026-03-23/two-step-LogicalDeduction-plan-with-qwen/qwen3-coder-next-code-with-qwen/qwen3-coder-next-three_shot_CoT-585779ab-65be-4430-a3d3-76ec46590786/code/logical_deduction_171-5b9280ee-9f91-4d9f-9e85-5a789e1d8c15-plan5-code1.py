from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define the variables (the seven golfers) and the domain (their finish positions)
# 1 = first place (highest/best), 7 = seventh place (lowest/worst)
golfers = ["Ana", "Eli", "Mya", "Amy", "Joe", "Mel", "Ada"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add constraints based on the puzzle's statements
# 1. All golfers must have a unique finish position
problem.addConstraint(AllDifferentConstraint())

# 2. "Ada finished above Mel" → Ada's position < Mel's position
problem.addConstraint(lambda ada, mel: ada < mel, ("Ada", "Mel"))

# 3. "Ada finished third-to-last" → With 7 golfers, third-to-last is position 5
problem.addConstraint(lambda ada: ada == 5, ("Ada",))

# 4. "Amy finished above Ana" → Amy's position < Ana's position
problem.addConstraint(lambda amy, ana: amy < ana, ("Amy", "Ana"))

# 5. "Mya finished second-to-last" → Mya's position = 6
problem.addConstraint(lambda mya: mya == 6, ("Mya",))

# 6. "Joe finished above Amy" → Joe's position < Amy's position
problem.addConstraint(lambda joe, amy: joe < amy, ("Joe", "Amy"))

# 7. "Eli finished below Ana" → Eli's position > Ana's position
problem.addConstraint(lambda eli, ana: eli > ana, ("Eli", "Ana"))

# Find the unique solution
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

# Find which golfer is in position 3 (third place)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 3:
            print(letter)