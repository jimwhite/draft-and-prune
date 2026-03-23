from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7, where 1 = first, 7 = last)
golfers = ["Joe", "Mel", "Mya", "Eve", "Rob", "Ada", "Dan"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add constraints based on the statements
# 1. All golfers have different finishing positions
problem.addConstraint(AllDifferentConstraint())

# 2. Rob finished first
problem.addConstraint(lambda Rob: Rob == 1, ["Rob"])

# 3. Eve finished last
problem.addConstraint(lambda Eve: Eve == 7, ["Eve"])

# 4. Dan finished above Ada (Dan's position number < Ada's position number)
problem.addConstraint(lambda Dan, Ada: Dan < Ada, ["Dan", "Ada"])

# 5. Mel finished above Mya (Mel's position number < Mya's position number)
problem.addConstraint(lambda Mel, Mya: Mel < Mya, ["Mel", "Mya"])

# 6. Joe finished second-to-last (position 6)
problem.addConstraint(lambda Joe: Joe == 6, ["Joe"])

# 7. Mya finished third (position 3)
problem.addConstraint(lambda Mya: Mya == 3, ["Mya"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    "A": "Joe",
    "B": "Mel",
    "C": "Mya",
    "D": "Eve",
    "E": "Rob",
    "F": "Ada",
    "G": "Dan"
}

# Find which golfer finished third (position 3)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 3:
            print(letter)