from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define the variables (the five vehicles) and the domain (their age rank)
# Let's use ranks 1 to 5, where 1 is the oldest and 5 is the newest.
vehicles = ["hatchback", "limousine", "sedan", "bus", "tractor"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add constraints based on the puzzle's statements
# 1. All vehicles must have a different age rank.
problem.addConstraint(AllDifferentConstraint())

# 2. "The tractor is newer than the hatchback." (Hatchback's rank is smaller)
problem.addConstraint(lambda hatchback, tractor: hatchback < tractor, ("hatchback", "tractor"))

# 3. "The bus is the second-oldest." (Rank 2)
problem.addConstraint(lambda bus: bus == 2, ("bus",))

# 4. "The hatchback is newer than the sedan." (Sedan's rank is smaller)
problem.addConstraint(lambda sedan, hatchback: sedan < hatchback, ("sedan", "hatchback"))

# 5. "The limousine is the newest." (Rank 5)
problem.addConstraint(lambda limousine: limousine == 5, ("limousine",))

# Find the unique solution to the problem
solutions = problem.getSolutions()

# The question asks which vehicle is the "oldest".
# In our ranking system (1=oldest), the oldest has a rank of 1.
choices = {
    "A": "hatchback",
    "B": "limousine",
    "C": "sedan",
    "D": "bus",
    "E": "tractor"
}

# Check the solution to find the vehicle with rank 1 and print the corresponding letter.
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 1:
            print(letter)