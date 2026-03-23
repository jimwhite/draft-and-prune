from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define the variables (the seven vehicles) and the domain (their age rank)
# Let's use ranks 1 to 7, where 1 is the oldest and 7 is the newest.
vehicles = ["truck", "hatchback", "minivan", "bus", "tractor", "station_wagon", "convertible"]
ranks = range(1, 8)
problem.addVariables(vehicles, ranks)

# Add constraints based on the puzzle's statements
# 1. All vehicles must have a different age rank.
problem.addConstraint(AllDifferentConstraint())

# 2. "The station wagon is the fourth-newest." (newest=7, so fourth-newest = 7-3 = 4)
problem.addConstraint(lambda station_wagon: station_wagon == 4, ("station_wagon",))

# 3. "The minivan is the third-newest." (third-newest = 7-2 = 5)
problem.addConstraint(lambda minivan: minivan == 5, ("minivan",))

# 4. "The tractor is the second-oldest." (second-oldest = 2)
problem.addConstraint(lambda tractor: tractor == 2, ("tractor",))

# 5. "The convertible is older than the station wagon." (convertible < station_wagon)
problem.addConstraint(lambda convertible, station_wagon: convertible < station_wagon, ("convertible", "station_wagon"))

# 6. "The truck is newer than the bus." (truck > bus, since newer = larger rank number)
problem.addConstraint(lambda bus, truck: bus < truck, ("bus", "truck"))

# 7. "The hatchback is older than the convertible." (hatchback < convertible)
problem.addConstraint(lambda hatchback, convertible: hatchback < convertible, ("hatchback", "convertible"))

# Find the unique solution to the problem
solutions = problem.getSolutions()

# The question asks which vehicle is the "second-newest".
# In our ranking system (1=oldest, 7=newest), second-newest has rank 6.
choices = {
    "A": "truck",
    "B": "hatchback",
    "C": "minivan",
    "D": "bus",
    "E": "tractor",
    "F": "station_wagon",
    "G": "convertible"
}

# Check the solution to find the vehicle with rank 6 and print the corresponding letter.
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 6:
            print(letter)