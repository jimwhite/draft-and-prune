from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define the variables (the seven golfers) and the domain (their finishing positions)
golfers = ["Ana", "Eli", "Mya", "Amy", "Joe", "Mel", "Ada"]
positions = range(1, 8)  # 1 = best (first place), 7 = worst (seventh place)
problem.addVariables(golfers, positions)

# Add constraints based on the problem description
# 1. All golfers must have different finishing positions
problem.addConstraint(AllDifferentConstraint())

# 2. "Ada finished above Mel" → Ada's position < Mel's position
problem.addConstraint(lambda Ada, Mel: Ada < Mel, ["Ada", "Mel"])

# 3. "Ada finished third-to-last" → With 7 golfers, third-to-last is position 5
problem.addConstraint(lambda Ada: Ada == 5, ["Ada"])

# 4. "Amy finished above Ana" → Amy's position < Ana's position
problem.addConstraint(lambda Amy, Ana: Amy < Ana, ["Amy", "Ana"])

# 5. "Mya finished second-to-last" → position 6
problem.addConstraint(lambda Mya: Mya == 6, ["Mya"])

# 6. "Joe finished above Amy" → Joe's position < Amy's position
problem.addConstraint(lambda Joe, Amy: Joe < Amy, ["Joe", "Amy"])

# 7. "Eli finished below Ana" → Eli's position > Ana's position
problem.addConstraint(lambda Eli, Ana: Eli > Ana, ["Eli", "Ana"])

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