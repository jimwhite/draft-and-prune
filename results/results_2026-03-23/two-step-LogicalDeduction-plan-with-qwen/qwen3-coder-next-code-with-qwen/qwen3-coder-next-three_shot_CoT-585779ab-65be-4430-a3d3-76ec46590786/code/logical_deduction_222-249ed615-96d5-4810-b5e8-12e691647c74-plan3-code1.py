from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define the variables (the seven vehicles) and their age ranks (1=oldest, 7=newest)
vehicles = ["truck", "hatchback", "minivan", "bus", "tractor", "station_wagon", "convertible"]
ranks = range(1, 8)
problem.addVariables(vehicles, ranks)

# Add constraints based on the puzzle's statements
# 1. All vehicles must have a different age rank.
problem.addConstraint(AllDifferentConstraint())

# 2. "The station wagon is the fourth-newest." (4th-newest means rank 4)
problem.addConstraint(lambda station_wagon: station_wagon == 4, ("station_wagon",))

# 3. "The minivan is the third-newest." (3rd-newest means rank 5)
problem.addConstraint(lambda minivan: minivan == 5, ("minivan",))

# 4. "The tractor is the second-oldest." (2nd-oldest means rank 2)
problem.addConstraint(lambda tractor: tractor == 2, ("tractor",))

# 5. "The convertible is older than the station wagon." (convertible rank < station_wagon rank)
problem.addConstraint(lambda convertible, station_wagon: convertible < station_wagon, ("convertible", "station_wagon"))

# 6. "The truck is newer than the bus." (bus rank < truck rank)
problem.addConstraint(lambda bus, truck: bus < truck, ("bus", "truck"))

# 7. "The hatchback is older than the convertible." (hatchback rank < convertible rank)
problem.addConstraint(lambda hatchback, convertible: hatchback < convertible, ("hatchback", "convertible"))

# Find the solution(s)
solutions = problem.getSolutions()

# Map choice letters to vehicle names
choices = {
    "A": "truck",
    "B": "hatchback",
    "C": "minivan",
    "D": "bus",
    "E": "tractor",
    "F": "station_wagon",
    "G": "convertible"
}

# Find which vehicle has rank 1 (oldest) and print the corresponding letter
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 1:
            print(letter)