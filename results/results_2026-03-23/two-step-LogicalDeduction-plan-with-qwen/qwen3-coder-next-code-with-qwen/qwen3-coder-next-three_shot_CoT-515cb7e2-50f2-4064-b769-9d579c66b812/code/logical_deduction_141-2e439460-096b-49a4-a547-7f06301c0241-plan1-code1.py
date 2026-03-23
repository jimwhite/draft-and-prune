from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (ranks 1 to 7, where 1 is first place)
golfers = ["Joe", "Rob", "Eli", "Dan", "Mya", "Ada", "Ana"]
ranks = range(1, 8)
problem.addVariables(golfers, ranks)

# Add AllDifferent constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# Joe finished above Ana → Joe's rank < Ana's rank
problem.addConstraint(lambda Joe, Ana: Joe < Ana, ["Joe", "Ana"])

# Ana finished second-to-last → position 6
problem.addConstraint(lambda Ana: Ana == 6, ["Ana"])

# Mya finished fourth → position 4
problem.addConstraint(lambda Mya: Mya == 4, ["Mya"])

# Dan finished third → position 3
problem.addConstraint(lambda Dan: Dan == 3, ["Dan"])

# Ada finished second → position 2
problem.addConstraint(lambda Ada: Ada == 2, ["Ada"])

# Eli finished third-to-last → position 5 (since last=7, second-to-last=6, third-to-last=5)
problem.addConstraint(lambda Eli: Eli == 5, ["Eli"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    "A": "Joe",
    "B": "Rob",
    "C": "Eli",
    "D": "Dan",
    "E": "Mya",
    "F": "Ada",
    "G": "Ana"
}

# Find who finished last (rank 7)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 7:
            print(letter)