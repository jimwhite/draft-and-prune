from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7, where 1 = first place)
golfers = ["Eli", "Eve", "Mel", "Joe", "Mya", "Rob", "Ada"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# Ada finished above Mya → Ada's position < Mya's position
problem.addConstraint(lambda ada, mya: ada < mya, ("Ada", "Mya"))

# Eli finished below Joe → Eli's position > Joe's position
problem.addConstraint(lambda eli, joe: eli > joe, ("Eli", "Joe"))

# Eli finished above Eve → Eli's position < Eve's position
problem.addConstraint(lambda eli, eve: eli < eve, ("Eli", "Eve"))

# Ada finished second-to-last → position = 6
problem.addConstraint(lambda ada: ada == 6, ("Ada",))

# Mel finished third → position = 3
problem.addConstraint(lambda mel: mel == 3, ("Mel",))

# Rob finished fourth → position = 4
problem.addConstraint(lambda rob: rob == 4, ("Rob",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    'A': "Eli",
    'B': "Eve",
    'C': "Mel",
    'D': "Joe",
    'E': "Mya",
    'F': "Rob",
    'G': "Ada"
}

# Find which golfer finished second (position = 2)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 2:
            print(letter)