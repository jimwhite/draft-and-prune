from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define the variables (the seven golfers) and their domain (positions 1 to 7)
# 1 = highest position (first place), 7 = lowest position (last place)
golfers = ["Eli", "Eve", "Mel", "Joe", "Mya", "Rob", "Ada"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add constraints based on the statements
# 1. All golfers must have distinct positions
problem.addConstraint(AllDifferentConstraint())

# 2. "Ada finished above Mya" → Ada's position < Mya's position
problem.addConstraint(lambda Ada, Mya: Ada < Mya, ("Ada", "Mya"))

# 3. "Eli finished below Joe" → Joe's position < Eli's position
problem.addConstraint(lambda Joe, Eli: Joe < Eli, ("Joe", "Eli"))

# 4. "Eli finished above Eve" → Eli's position < Eve's position
problem.addConstraint(lambda Eli, Eve: Eli < Eve, ("Eli", "Eve"))

# 5. "Ada finished second-to-last" → Ada's position = 6
problem.addConstraint(lambda Ada: Ada == 6, ("Ada",))

# 6. "Mel finished third" → Mel's position = 3
problem.addConstraint(lambda Mel: Mel == 3, ("Mel",))

# 7. "Rob finished fourth" → Rob's position = 4
problem.addConstraint(lambda Rob: Rob == 4, ("Rob",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    "A": "Eli",
    "B": "Eve",
    "C": "Mel",
    "D": "Joe",
    "E": "Mya",
    "F": "Rob",
    "G": "Ada"
}

# Find which golfer finished second-to-last (position 6)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 6:
            print(letter)