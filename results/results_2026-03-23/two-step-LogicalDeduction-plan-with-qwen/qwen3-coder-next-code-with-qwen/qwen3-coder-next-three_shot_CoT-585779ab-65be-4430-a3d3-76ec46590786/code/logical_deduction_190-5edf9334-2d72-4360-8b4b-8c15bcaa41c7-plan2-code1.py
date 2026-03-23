from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define the variables (the seven golfers) and their domain (finishing positions 1-7)
golfers = ["Dan", "Eve", "Mya", "Amy", "Rob", "Ada", "Joe"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add constraints based on the problem description
# 1. All golfers must have unique finishing positions
problem.addConstraint(AllDifferentConstraint())

# 2. "Amy finished third"
problem.addConstraint(lambda Amy: Amy == 3, ["Amy"])

# 3. "Joe finished last"
problem.addConstraint(lambda Joe: Joe == 7, ["Joe"])

# 4. "Mya finished above Dan" (Mya's position number is less than Dan's)
problem.addConstraint(lambda Mya, Dan: Mya < Dan, ["Mya", "Dan"])

# 5. "Eve finished fourth"
problem.addConstraint(lambda Eve: Eve == 4, ["Eve"])

# 6. "Amy finished above Rob" (Amy's position number is less than Rob's)
problem.addConstraint(lambda Amy, Rob: Amy < Rob, ["Amy", "Rob"])

# 7. "Ada finished third-to-last" (in a field of 7, third-to-last is position 5)
problem.addConstraint(lambda Ada: Ada == 5, ["Ada"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    "A": "Dan",
    "B": "Eve",
    "C": "Mya",
    "D": "Amy",
    "E": "Rob",
    "F": "Ada",
    "G": "Joe"
}

# Find which golfer finished third (position 3) and print the corresponding choice letter
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 3:
            print(letter)