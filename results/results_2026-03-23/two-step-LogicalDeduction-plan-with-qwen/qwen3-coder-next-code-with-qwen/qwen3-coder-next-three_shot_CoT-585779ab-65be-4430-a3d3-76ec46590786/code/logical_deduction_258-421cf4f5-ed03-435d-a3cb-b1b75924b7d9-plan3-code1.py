from constraint import *

problem = Problem()

vehicles = ["tractor", "truck", "minivan"]
positions = range(1, 4)
problem.addVariables(vehicles, positions)

problem.addConstraint(AllDifferentConstraint())

problem.addConstraint(lambda tr, tu: tr < tu, ["tractor", "truck"])

problem.addConstraint(lambda tu, mi: tu < mi, ["truck", "minivan"])

solutions = problem.getSolutions()

choices = {
    "A": "tractor",
    "B": "truck",
    "C": "minivan"
}

for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 2:
            print(letter)