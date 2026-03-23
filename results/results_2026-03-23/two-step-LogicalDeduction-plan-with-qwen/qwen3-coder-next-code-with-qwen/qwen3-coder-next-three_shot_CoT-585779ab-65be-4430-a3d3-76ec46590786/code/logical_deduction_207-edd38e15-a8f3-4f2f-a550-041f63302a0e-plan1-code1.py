from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7, where 1 is highest rank)
golfers = ["Eli", "Eve", "Mel", "Joe", "Mya", "Rob", "Ada"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "Ada finished above Mya" → Ada < Mya
problem.addConstraint(lambda Ada, Mya: Ada < Mya, ("Ada", "Mya"))

# "Eli finished below Joe" → Joe < Eli
problem.addConstraint(lambda Joe, Eli: Joe < Eli, ("Joe", "Eli"))

# "Eli finished above Eve" → Eli < Eve
problem.addConstraint(lambda Eli, Eve: Eli < Eve, ("Eli", "Eve"))

# "Ada finished second-to-last" → Ada == 6
problem.addConstraint(lambda Ada: Ada == 6, ("Ada",))

# "Mel finished third" → Mel == 3
problem.addConstraint(lambda Mel: Mel == 3, ("Mel",))

# "Rob finished fourth" → Rob == 4
problem.addConstraint(lambda Rob: Rob == 4, ("Rob",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfers
choices = {
    'A': "Eli",
    'B': "Eve",
    'C': "Mel",
    'D': "Joe",
    'E': "Mya",
    'F': "Rob",
    'G': "Ada"
}

# Find which golfer has position 6 (second-to-last)
for solution in solutions:
    for letter, golfer in choices.items():
        if solution[golfer] == 6:
            print(letter)