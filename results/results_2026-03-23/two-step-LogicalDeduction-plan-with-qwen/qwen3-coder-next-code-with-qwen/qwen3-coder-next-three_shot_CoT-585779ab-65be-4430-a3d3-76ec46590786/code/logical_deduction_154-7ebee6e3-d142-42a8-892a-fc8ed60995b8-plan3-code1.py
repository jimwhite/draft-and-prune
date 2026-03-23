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

# Joe finished third
problem.addConstraint(lambda Joe: Joe == 3, ["Joe"])

# Dan finished last
problem.addConstraint(lambda Dan: Dan == 7, ["Dan"])

# Eve finished first
problem.addConstraint(lambda Eve: Eve == 1, ["Eve"])

# Mel finished below Rob (Mel's rank is worse/higher than Rob's)
problem.addConstraint(lambda Mel, Rob: Mel > Rob, ["Mel", "Rob"])

# Ada finished above Joe (Ada's rank is better/lower than Joe's)
problem.addConstraint(lambda Ada: Ada < 3, ["Ada"])

# Rob finished third-to-last (position 5 in a field of 7)
problem.addConstraint(lambda Rob: Rob == 5, ["Rob"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfers
choices = {
    'A': "Amy",
    'B': "Eve",
    'C': "Ada",
    'D': "Rob",
    'E': "Dan",
    'F': "Mel",
    'G': "Joe"
}

# Find who finished fourth (rank 4)
for solution in solutions:
    for letter, golfer in choices.items():
        if solution[golfer] == 4:
            print(letter)