from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define the variables (the five vehicles) and the domain (their age rank)
# Let's use ranks 1 to 5, where 1 is the oldest and 5 is the newest.
vehicles = ["minivan", "limousine", "sedan", "tractor", "hatchback"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add constraints based on the puzzle's statements
# 1. All vehicles must have a different age rank.
problem.addConstraint(AllDifferentConstraint())

# 2. "The tractor is the second-newest." (Rank 4)
problem.addConstraint(lambda tractor: tractor == 4, ("tractor",))

# 3. "The limousine is newer than the hatchback." (hatchback < limousine)
problem.addConstraint(lambda hatchback, limousine: hatchback < limousine, ("hatchback", "limousine"))

# 4. "The limousine is older than the sedan." (limousine < sedan)
problem.addConstraint(lambda limousine, sedan: limousine < sedan, ("limousine", "sedan"))

# 5. "The minivan is newer than the sedan." (sedan < minivan)
problem.addConstraint(lambda sedan, minivan: sedan < minivan, ("sedan", "minivan"))

# Find the unique solution to the problem
solutions = problem.getSolutions()

# The question asks which vehicle is the "second-oldest".
# In our ranking system (1=oldest), the second-oldest has a rank of 2.
choices = {
    "A": "minivan",
    "B": "limousine",
    "C": "sedan",
    "D": "tractor",
    "E": "hatchback"
}

# Check the solution to find the vehicle with rank 2 and print the corresponding letter.
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 2:
            print(letter)