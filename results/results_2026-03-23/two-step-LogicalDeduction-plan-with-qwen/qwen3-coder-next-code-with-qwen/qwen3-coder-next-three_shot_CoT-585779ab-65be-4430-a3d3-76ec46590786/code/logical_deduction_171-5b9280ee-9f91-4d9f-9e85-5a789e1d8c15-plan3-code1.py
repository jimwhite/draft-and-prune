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
# "Ada finished above Mel" → Ada < Mel
problem.addConstraint(lambda Ada, Mel: Ada < Mel, ("Ada", "Mel"))

# "Ada finished third-to-last" → position 5 (since 7-2=5)
problem.addConstraint(lambda Ada: Ada == 5, ("Ada",))

# "Amy finished above Ana" → Amy < Ana
problem.addConstraint(lambda Amy, Ana: Amy < Ana, ("Amy", "Ana"))

# "Mya finished second-to-last" → position 6
problem.addConstraint(lambda Mya: Mya == 6, ("Mya",))

# "Joe finished above Amy" → Joe < Amy
problem.addConstraint(lambda Joe, Amy: Joe < Amy, ("Joe", "Amy"))

# "Eli finished below Ana" → Eli > Ana
problem.addConstraint(lambda Eli, Ana: Eli > Ana, ("Eli", "Ana"))

# Solve the problem
solutions = problem.getSolutions()

# Map golfers to choice letters
golfer_to_choice = {
    "Ana": "A",
    "Eli": "B",
    "Mya": "C",
    "Amy": "D",
    "Joe": "E",
    "Mel": "F",
    "Ada": "G"
}

# Find who finished third (position 3)
for solution in solutions:
    for golfer, choice_letter in golfer_to_choice.items():
        if solution[golfer] == 3:
            print(choice_letter)