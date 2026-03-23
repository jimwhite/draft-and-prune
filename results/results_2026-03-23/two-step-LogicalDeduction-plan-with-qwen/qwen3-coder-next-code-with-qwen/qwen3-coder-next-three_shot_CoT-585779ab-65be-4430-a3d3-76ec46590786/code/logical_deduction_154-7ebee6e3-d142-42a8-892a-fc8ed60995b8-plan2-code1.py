from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7, where 1 = first place)
golfers = ["amy", "eve", "ada", "rob", "dan", "mel", "joe"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "Joe finished third"
problem.addConstraint(lambda joe: joe == 3, ["joe"])

# "Dan finished last"
problem.addConstraint(lambda dan: dan == 7, ["dan"])

# "Eve finished first"
problem.addConstraint(lambda eve: eve == 1, ["eve"])

# "Mel finished below Rob" (Rob placed higher than Mel)
problem.addConstraint(lambda rob, mel: rob < mel, ["rob", "mel"])

# "Ada finished above Joe" (Ada placed higher than Joe)
problem.addConstraint(lambda ada, joe: ada < joe, ["ada", "joe"])

# "Rob finished third-to-last" (position 5 in a 7-person race)
problem.addConstraint(lambda rob: rob == 5, ["rob"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    'A': 'amy',
    'B': 'eve',
    'C': 'ada',
    'D': 'rob',
    'E': 'dan',
    'F': 'mel',
    'G': 'joe'
}

# Find which golfer finished in position 4
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 4:
            print(letter)