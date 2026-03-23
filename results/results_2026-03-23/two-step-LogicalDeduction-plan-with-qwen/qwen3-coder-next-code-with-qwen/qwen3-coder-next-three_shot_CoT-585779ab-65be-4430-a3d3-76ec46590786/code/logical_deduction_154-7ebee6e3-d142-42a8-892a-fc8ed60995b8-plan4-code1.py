from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (ranks 1 to 7, where 1 = first place)
golfers = ["Amy", "Eve", "Ada", "Rob", "Dan", "Mel", "Joe"]
ranks = range(1, 8)
problem.addVariables(golfers, ranks)

# Add constraints
# All golfers have different ranks
problem.addConstraint(AllDifferentConstraint())

# "Joe finished third"
problem.addConstraint(lambda Joe: Joe == 3, ["Joe"])

# "Dan finished last"
problem.addConstraint(lambda Dan: Dan == 7, ["Dan"])

# "Eve finished first"
problem.addConstraint(lambda Eve: Eve == 1, ["Eve"])

# "Mel finished below Rob" (Mel's rank > Rob's rank)
problem.addConstraint(lambda Mel, Rob: Mel > Rob, ["Mel", "Rob"])

# "Ada finished above Joe" (Ada's rank < Joe's rank = 3)
problem.addConstraint(lambda Ada: Ada < 3, ["Ada"])

# "Rob finished third-to-last" (in a 7-person field: position 5)
problem.addConstraint(lambda Rob: Rob == 5, ["Rob"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    'A': "Amy",
    'B': "Eve",
    'C': "Ada",
    'D': "Rob",
    'E': "Dan",
    'F': "Mel",
    'G': "Joe"
}

# Find which golfer has rank 4 (fourth place)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 4:
            print(letter)