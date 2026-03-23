from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (ranks 1 to 7, where 1 is best)
golfers = ["Ana", "Eli", "Mya", "Amy", "Joe", "Mel", "Ada"]
ranks = range(1, 8)
problem.addVariables(golfers, ranks)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "Ada finished above Mel" → Ada < Mel
problem.addConstraint(lambda Ada, Mel: Ada < Mel, ("Ada", "Mel"))

# "Ada finished third-to-last" → In 7 golfers, third-to-last is rank 5
problem.addConstraint(lambda Ada: Ada == 5, ("Ada",))

# "Amy finished above Ana" → Amy < Ana
problem.addConstraint(lambda Amy, Ana: Amy < Ana, ("Amy", "Ana"))

# "Mya finished second-to-last" → rank 6
problem.addConstraint(lambda Mya: Mya == 6, ("Mya",))

# "Joe finished above Amy" → Joe < Amy
problem.addConstraint(lambda Joe, Amy: Joe < Amy, ("Joe", "Amy"))

# "Eli finished below Ana" → Eli > Ana
problem.addConstraint(lambda Eli, Ana: Eli > Ana, ("Eli", "Ana"))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfers
choices = {
    "A": "Ana",
    "B": "Eli",
    "C": "Mya",
    "D": "Amy",
    "E": "Joe",
    "F": "Mel",
    "G": "Ada"
}

# Find which golfer has rank 3 (third place)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 3:
            print(letter)