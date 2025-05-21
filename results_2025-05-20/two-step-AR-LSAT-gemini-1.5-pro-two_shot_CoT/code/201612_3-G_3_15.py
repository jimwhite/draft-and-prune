from z3 import *

# Constants
F, G, H, I = 0, 1, 2, 3
O, W = 0, 1
F_O, F_W, G_O, G_W, H_O, H_W, I_O, I_W = 0, 1, 2, 3, 4, 5, 6, 7
W1, W2, W3, W4 = 0, 1, 2, 3
U, L = 0, 1

# Variable
pos_to_painting = Array('pos_to_painting', IntSort(), IntSort())

# Helper functions
def student_of(painting_id):
    return painting_id / 2 # Fixed: Use / for division in Z3

def type_of(painting_id):
    return painting_id % 2

def wall_of(position_id):
    return position_id / 2 # Fixed: Use / for division in Z3

def pos_type_of(position_id):
    return position_id % 2

# Solver
solver = Solver()

# Base Constraints
solver.add(Distinct([pos_to_painting[i] for i in range(8)]))
i = Int('i') # Declare i for the ForAll quantifier
solver.add(ForAll([i], Implies(And(i >= 0, i < 8), And(pos_to_painting[i] >= 0, pos_to_painting[i] <= 7)))) # Fixed: Added implication and range check for i

for w in range(4):
    solver.add(Or(type_of(pos_to_painting[w*2 + U]) == O, type_of(pos_to_painting[w*2 + L]) == O))
    solver.add(student_of(pos_to_painting[w*2 + U]) != student_of(pos_to_painting[w*2 + L]))
    solver.add(Not(And(student_of(pos_to_painting[w*2 + U]) == F, student_of(pos_to_painting[w*2 + L]) == I)))
    solver.add(Not(And(student_of(pos_to_painting[w*2 + U]) == I, student_of(pos_to_painting[w*2 + L]) == F)))

pos_GW = Int('pos_GW')
pos_FO = Int('pos_FO')
solver.add(Exists([pos_GW, pos_FO], And(pos_to_painting[pos_GW] == G_W, pos_type_of(pos_GW) == U, pos_to_painting[pos_FO] == F_O, wall_of(pos_GW) == wall_of(pos_FO))))

solver.add(pos_to_painting[W4*2 + L] == I_O)

# Question Condition
pos_GO = Int('pos_GO')
pos_FW = Int('pos_FW')
solver.add(Exists([pos_GO, pos_FW], And(pos_to_painting[pos_GO] == G_O, pos_to_painting[pos_FW] == F_W, wall_of(pos_GO) == wall_of(pos_FW))))


# Answer Choices
answer_choices = [
    Exists([pos_GO], And(pos_to_painting[pos_GO] == G_O, pos_type_of(pos_GO) == U)),
    Exists([pos_HW, pos_IW], And(pos_to_painting[pos_HW] == H_W, pos_to_painting[pos_IW] == I_W, wall_of(pos_HW) == wall_of(pos_IW))),
    Exists([pos_HO], And(pos_to_painting[pos_HO] == H_O, pos_type_of(pos_HO) == U)),
    Exists([pos_HO, pos_IW], And(pos_to_painting[pos_HO] == H_O, pos_to_painting[pos_IW] == I_W, wall_of(pos_HO) == wall_of(pos_IW))),
    Exists([pos_IW], And(pos_to_painting[pos_IW] == I_W, pos_type_of(pos_IW) == L))
]
pos_HW, pos_IW, pos_HO = Ints('pos_HW pos_IW pos_HO')


for i, choice in enumerate(answer_choices):
    solver.push()
    solver.add(Not(choice))
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
