from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define the variables (the seven vehicles) and their domain (age ranks)
# 1 = oldest, 7 = newest
vehicles = ["convertible", "limousine", "hatchback", "bus", "station_wagon", "tractor", "minivan"]
ranks = range(1, 8)
problem.addVariables(vehicles, ranks)

# Add constraints based on the puzzle's statements
# 1. All vehicles must have a different age rank.
problem.addConstraint(AllDifferentConstraint())

# 2. "The station wagon is the fourth-newest." (newest=7, so fourth-newest = 7-3 = 4)
problem.addConstraint(lambda station_wagon: station_wagon == 4, ("station_wagon",))

# 3. "The hatchback is older than the bus." (hatchback < bus)
problem.addConstraint(lambda hatchback, bus: hatchback < bus, ("hatchback", "bus"))

# 4. "The hatchback is the second-newest." (second-newest = 6)
problem.addConstraint(lambda hatchback: hatchback == 6, ("hatchback",))

# 5. "The minivan is newer than the limousine." (limousine < minivan)
problem.addConstraint(lambda limousine, minivan: limousine < minivan, ("limousine", "minivan"))

# 6. "The convertible is older than the limousine." (convertible < limousine)
problem.addConstraint(lambda convertible, limousine: convertible < limousine, ("convertible", "limousine"))

# 7. "The tractor is the second-oldest." (second-oldest = 2)
problem.addConstraint(lambda tractor: tractor == 2, ("tractor",))

# Find the solution(s)
solutions = problem.getSolutions()

# Map choice letters to vehicle names
choices = {
    "A": "convertible",
    "B": "limousine",
    "C": "hatchback",
    "D": "bus",
    "E": "station_wagon",
    "F": "tractor",
    "G": "minivan"
}

# Find which vehicle is third-newest (rank = 5)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 5:
            print(letter)