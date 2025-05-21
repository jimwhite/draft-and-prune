from z3 import *

# Variables
composition_at_slot = Array('composition_at_slot', IntSort(), IntSort())
compositions = {'F': 0, 'H': 1, 'L': 2, 'O': 3, 'P': 4, 'R': 5, 'S': 6, 'T': 7}
solver = Solver()

# Constraints
i = Int('i')
j = Int('j')

solver.add(ForAll([i], And(composition_at_slot[i] >= 0, composition_at_slot[i] < 8))) # Constraint 0
solver.add(Distinct([composition_at_slot[i] for i in range(8)])) # Constraint 1
solver.add(Or(Exists([i], And(i >= 0, i < 7, composition_at_slot[i] == compositions['T'], composition_at_slot[i+1] == compositions['F'])), 
             Exists([i], And(i > 0, i <= 7, composition_at_slot[i] == compositions['T'], composition_at_slot[i-1] == compositions['R'])))) # Constraint 2
solver.add(Or(Exists([i, j], And(i >= 0, i < 8, j >= 0, j < 8, composition_at_slot[i] == compositions['F'], composition_at_slot[j] == compositions['R'], j - i > 2)),
             Exists([i, j], And(i >= 0, i < 8, j >= 0, j < 8, composition_at_slot[i] == compositions['F'], composition_at_slot[j] == compositions['R'], i - j > 2)))) # Constraint 3
solver.add(Or(composition_at_slot[0] == compositions['O'], composition_at_slot[4] == compositions['O'])) # Constraint 4
solver.add(Or(composition_at_slot[7] == compositions['L'], composition_at_slot[7] == compositions['H'])) # Constraint 5
solver.add(Exists([i, j], And(i >= 0, i < 8, j >= 0, j < 8, i < j, composition_at_slot[i] == compositions['P'], composition_at_slot[j] == compositions['S']))) # Constraint 6
solver.add(Exists([i, j], And(i >= 0, i < 8, j >= 0, j < 8, Or(j - i > 1, i - j > 1), composition_at_slot[i] == compositions['O'], composition_at_slot[j] == compositions['S']))) # Constraint 7
solver.add(Exists([i, j], And(i >= 0, i < 8, j >= 0, j < 8, j - i == 3, composition_at_slot[i] == compositions['F'], composition_at_slot[j] == compositions['O']))) # Constraint 8


# Answer choices
choices = ["first", "third", "fourth", "sixth", "seventh"]
slots = [0, 2, 3, 5, 6]

for i in range(len(choices)):
    solver.push()
    solver.add(composition_at_slot[slots[i]] == compositions['R'])
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()