from z3 import *

# Students: G, H, I, K, L, N, O, R
students = {'G': 0, 'H': 1, 'I': 2, 'K': 3, 'L': 4, 'N': 5, 'O': 6, 'R': 7}
num_students = len(students)

# Days: M, T, W
days = {'M': 0, 'T': 1, 'W': 2}
num_days = len(days)

# Slots: MxM, MxA, TxM, TxA, WxM, WxA
slots = [Int('slot_%i' % i) for i in range(num_days * 2)]

solver = Solver()

# Each slot is assigned to exactly one student
for slot in slots:
    solver.add(And(slot >= 0, slot < num_students))
solver.add(Distinct(slots))

# Constraint 1: George only on Tuesday
solver.add(Or(slots[2] == students['G'], slots[3] == students['G']))

# Constraint 2: No Olivia/Robert in afternoon
solver.add(slots[1] != students['O'])
solver.add(slots[3] != students['O'])
solver.add(slots[5] != students['O'])
solver.add(slots[1] != students['R'])
solver.add(slots[3] != students['R'])
solver.add(slots[5] != students['R'])


options = [
    [('H', 0), ('R', 1), ('O', 2), ('I', 3), ('L', 4), ('K', 5)],
    [('I', 0), ('O', 1), ('H', 2), ('K', 3), ('N', 4), ('L', 5)],
    [('L', 0), ('H', 1), ('G', 2), ('K', 3), ('R', 4), ('I', 5)],
    [('N', 0), ('H', 1), ('R', 2), ('I', 3), ('O', 4), ('L', 5)],
    [('O', 0), ('N', 1), ('I', 2), ('H', 3), ('K', 4), ('G', 5)]
]

for option_index, option in enumerate(options):
    solver.push()
    for student_initial, slot_index in option:
        solver.add(slots[slot_index] == students[student_initial])

    # Constraint 3: Nina triggers Helen & Irving next day (unless Wednesday)
    nina_slots = [slot_index for student_initial, slot_index in option if student_initial == 'N']
    if nina_slots:
        nina_slot = nina_slots[0]
        if nina_slot < 4:  # Not Wednesday
            next_day_slots = [nina_slot + 2, nina_slot + 3]
            solver.add(Or(slots[next_day_slots[0]] == students['H'], slots[next_day_slots[1]] == students['H']))
            solver.add(Or(slots[next_day_slots[0]] == students['I'], slots[next_day_slots[1]] == students['I']))

    if solver.check() == sat:
        print(f"Option {chr(65 + option_index)} is correct")
        exit()
    solver.pop()