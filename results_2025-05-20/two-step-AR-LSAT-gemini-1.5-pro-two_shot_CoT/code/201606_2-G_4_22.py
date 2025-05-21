from z3 import *

# 1. Entities (Singer IDs and Slot Indices defined in the plan)
K = 0
L = 1
T = 2
W = 3
Y = 4
Z = 5

# 2. Variables
audition_schedule = Array('audition_schedule', IntSort(), IntSort())
recorded = Array('recorded', IntSort(), BoolSort())

# 3. Constraints
solver = Solver()
i = Int('i')
slot_W = Int('slot_W')
slot_K = Int('slot_K')
slot_T = Int('slot_T')
slot_Z = Int('slot_Z')
slot_Y = Int('slot_Y')


solver.add(ForAll(i, Implies(And(i >= 0, i < 6), And(audition_schedule[i] >= 0, audition_schedule[i] < 6)))) # Constraint 0
solver.add(Distinct([audition_schedule[i] for i in range(6)])) # Constraint 1
solver.add(ForAll(i, Implies(And(i >= 0, i < 6), recorded[i] == Or(audition_schedule[i] == K, audition_schedule[i] == L)))) # Constraint 2 & 3
solver.add(recorded[3] == False) # Constraint 4
solver.add(recorded[4] == True) # Constraint 5
solver.add(Exists(slot_W, And(slot_W >= 0, slot_W < 6, audition_schedule[slot_W] == W, ForAll(i, Implies(And(i >= 0, i < 6, recorded[i] == True), slot_W < i))))) # Constraint 6
solver.add(Exists(slot_K, Exists(slot_T, And(slot_K >= 0, slot_K < 6, audition_schedule[slot_K] == K, slot_T >= 0, slot_T < 6, audition_schedule[slot_T] == T, slot_K < slot_T)))) # Constraint 7
solver.add(Exists(slot_Z, Exists(slot_Y, And(slot_Z >= 0, slot_Z < 6, audition_schedule[slot_Z] == Z, slot_Y >= 0, slot_Y < 6, audition_schedule[slot_Y] == Y, slot_Z < slot_Y)))) # Constraint 8


# 4. Answering the Question
possible_slots = []
answer_choices = ["fifth", "fourth", "third", "second", "first"]
slot_indices = [4, 3, 2, 1, 0]  # Corresponding indices

for choice, index in zip(answer_choices, slot_indices):
    solver.push()
    solver.add(audition_schedule[index] == Y)
    if solver.check() == sat:
        possible_slots.append(choice)
    solver.pop()

if "fifth" in possible_slots:
    print("Option A is correct")
    exit()
if "fourth" in possible_slots:
    print("Option B is correct")
    exit()
if "third" in possible_slots:
    print("Option C is correct")
    exit()
if "second" in possible_slots:
    print("Option D is correct")
    exit()
if "first" in possible_slots:
    print("Option E is correct")
    exit()