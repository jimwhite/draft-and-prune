from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define the variables (the seven vehicles) and the domain (their age rank)
# Let's use ranks 1 to 7, where 1 is the oldest and 7 is the newest.
vehicles = ["convertible", "truck", "tractor", "limousine", "motorcycle", "hatchback", "sedan"]
ranks = range(1, 8)
problem.addVariables(vehicles, ranks)

# Add constraints based on the puzzle's statements
# 1. All vehicles must have a different age rank.
problem.addConstraint(AllDifferentConstraint())

# 2. "The hatchback is the fourth-newest." (Rank = 4)
problem.addConstraint(lambda hatchback: hatchback == 4, ("hatchback",))

# 3. "The limousine is older than the motorcycle." (limousine < motorcycle)
problem.addConstraint(lambda limousine, motorcycle: limousine < motorcycle, ("limousine", "motorcycle"))

# 4. "The truck is newer than the motorcycle." (truck > motorcycle)
problem.addConstraint(lambda truck, motorcycle: truck > motorcycle, ("truck", "motorcycle"))

# 5. "The sedan is the second-newest." (Rank = 6)
problem.addConstraint(lambda sedan: sedan == 6, ("sedan",))

# 6. "The tractor is newer than the convertible." (tractor > convertible)
problem.addConstraint(lambda tractor, convertible: tractor > convertible, ("tractor", "convertible"))

# 7. "The hatchback is older than the convertible." (hatchback < convertible)
problem.addConstraint(lambda hatchback, convertible: hatchback < convertible, ("hatchback", "convertible"))

# Find the unique solution to the problem
solutions = problem.getSolutions()

# The question asks which vehicle is the "third-newest".
# In our ranking system (1=oldest, 7=newest), third-newest corresponds to rank = 5.
choices = {
    "A": "convertible",
    "B": "truck",
    "C": "tractor",
    "D": "limousine",
    "E": "motorcycle",
    "F": "hatchback",
    "G": "sedan"
}

# Check the solution to find which vehicle has rank 5 and print the corresponding letter.
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 5:
            print(letter)