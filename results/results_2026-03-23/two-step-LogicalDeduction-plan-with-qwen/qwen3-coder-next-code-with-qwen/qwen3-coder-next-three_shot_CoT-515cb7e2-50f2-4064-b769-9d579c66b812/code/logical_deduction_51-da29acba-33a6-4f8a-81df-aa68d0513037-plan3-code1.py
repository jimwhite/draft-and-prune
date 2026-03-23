from constraint import *

problem = Problem()

vehicles = ["minivan", "hatchback", "bus", "convertible", "motorcycle"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

problem.addConstraint(AllDifferentConstraint())

problem.addConstraint(lambda hatchback, convertible: hatchback > convertible, ("hatchback", "convertible"))
problem.addConstraint(lambda bus, hatchback: bus > hatchback, ("bus", "hatchback"))
problem.addConstraint(lambda bus, motorcycle: bus < motorcycle, ("bus", "motorcycle"))
problem.addConstraint(lambda minivan: minivan == 5, ("minivan",))

solutions = problem.getSolutions()

choices = {
    "A": "minivan",
    "B": "hatchback",
    "C": "bus",
    "D": "convertible",
    "E": "motorcycle"
}

for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 5:
            print(letter)